from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from order.models import (
    UserOrderHystory,
)

from order.tools.minimize_products import minimize

from market.models import ProductsInAdress

from lk.models import (
    Adress,
)

from cart.models import (
    CartUser,
    ProductsInCart,
)

from settings.models import (
    OrderSettings,
)

from settings.tools.payment import (
    yoo_payment,
    is_payment,
)

# from settings.tools.telegram import (
#     # send_message_order,
# )

from order.tools.geo import (
    distance_between_coordinates,
)

from settings.tools.distribution import (
    Distribution,
)

# from order.tools.geo import find_nearest_addres

class CreateOrder(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        
        is_call = request.data["is_call"]
        adress_id = request.data["user_adress_id"]
        siti_id = request.data["siti_id"]
        total_price = 0.0
        total_price_discount = 0.0

        cart_user_data = []
        cart_user = CartUser.objects.get(user=user)

        adress_id = request.data["adress_id"]

        for product_in_cart in cart_user.products.all():
            product = product_in_cart.product

            product_in_adress = ProductsInAdress.objects.filter(adress=adress_id, products=product.pk).first()

            product_data = {
                "id": product.pk,
                "category": {
                    "id": product.category.pk,
                    "title": product.category.title
                    },
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "discount_price": round(product.price * ((1 - (product.discount / 100) if product.discount != 0 else 1)), 2),
                "discount_procent": product.discount,
                "weight": product.weight,
                "dimensions": {
                    "id": product.dimensions.pk,
                    "title": product.dimensions.title
                    },
                "fats": product.fats,
                "carbohydrates": product.carbohydrates,
                "proteins": product.proteins,
                "calories": product.calories,
                "storeg_temperature": product.storeg_temperature,
                "sheif_life": product.sheif_life,
                "image": f"/media/{product.image}",
                "is_activ": product.is_activ,
                "count": (product_in_adress.count if product_in_adress else None)
            }
            cart_user_data.append({
                "id": product_in_cart.pk,
                "product": product_data,
                "count": product_in_cart.count
                })

            total_price += product_data["price"] * product_in_cart.count
            total_price_discount += product_data["discount_price"] * product_in_cart.count

        # Получаем существующий объект CartUser

        # Создаем новый объект UserOrderHystory на основе данных из CartUser и передаем адресный идентификатор
        order = UserOrderHystory.create_order_from_cart_user(cart_user=cart_user, 
                                                             adress_id=adress_id, 
                                                             is_call=is_call,
                                                             siti_id=siti_id
                                                             )
        if isinstance(order, UserOrderHystory):

            minimize(order)

            # Сохраняем новый объект в базе данных
            payment = yoo_payment(order.price, order.pk, user.username)
            order.pyment_id = payment.id
            order.save()

            cart_user.products.clear()
            cart_user.save()

            return Response({"status": True, "order_id": order.pk, 
                             "payment_url": payment.confirmation.confirmation_url, 
                             "cart": cart_user_data, "price": round(total_price, 2), 
                             "price_discount": round(total_price_discount, 2)})
        else:
            return Response(order, status=status.HTTP_400_BAD_REQUEST)


class GetOrder(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        order_id = request.query_params.get("order_id")

        user_order = UserOrderHystory.objects.filter(pk=order_id).first()

        order_data = {
            "id": user_order.pk,
            "datetime": user_order.datetime,
            "price": int(user_order.price),
            "is_payment": user_order.is_pyment,
            "payment_url": f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={user_order.pyment_id}",
            "status": {
                "id": user_order.status.pk,
                "title": user_order.status.title
                },
            "products": [{
                "id": product.id,
                "price": product.product.price,
                "discount_price": round(product.product.price * ((1 - (product.product.discount / 100) if product.product.discount != 0 else 1)), 2),
                "discount_procent": product.product.discount,
                "title": product.product.title,
                "image": f"/media/{product.product.image}",
                "count": product.count,
                } for product in user_order.products.all()],
            "adress": str(user_order.user_adress),
        }

        return Response({"status": True, "order": order_data})


class ListOrder(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.filter(pk=request.user.id).first()
        user_order = UserOrderHystory.objects.filter(user=user)
        order_data = [{
            "id": i.pk,
            "datetime": i.datetime,
            "price": int(i.price),
            "is_payment": i.is_pyment,
            "payment_url": f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={i.pyment_id}",
            "status": {
                "id": i.status.pk,
                "title": i.status.title
                },
            "products": [{
                "id": product.id,
                "price": product.product.price,
                "discount_price": round(product.product.price * ((1 - (product.product.discount / 100) if product.product.discount != 0 else 1)), 2),
                "discount_procent": product.product.discount,
                "title": product.product.title,
                "image": f"/media/{product.product.image}",
                } for product in i.products.all()],
            "adress": str(i.user_adress),
        } for i in user_order]

        return Response({"status": True, "order": order_data})


# class OrderPaymentSuccess(APIView):
#     permission_classes = (IsAuthenticated, )

#     def post(self, request):
#         order_id = request.data["order_id"]
#         order = UserOrderHystory.objects.get(pk=order_id)
#         if is_payment(order.pyment_id):
#             order.is_pyment = True
#             order.save()
#             return Response({"status": True})
#         else:
#             return Response({"status": False, "error": "Not_paid"}, status=status.HTTP_402_PAYMENT_REQUIRED)
        

# class GetDeliveryType(APIView):
#     def get(self, request):
#         delivery_type = DeliveryType.objects.all()
#         delivery = [{
#             "id": i.pk,
#             "title": i.title
#         } for i in delivery_type]

#         return Response({"status": True, "delivery_list": delivery})


# class GetPaymentType(APIView):
#     def get(self, request):
#         payment_type = PymentType.objects.all()
#         payment = [{
#             "id": i.pk,
#             "title": i.title
#         } for i in payment_type]

#         return Response({"status": True, "payment_list": payment})


# class GetTypeDeliveryForCoord(APIView):
#     permission_classes = (IsAuthenticated, )
    
#     def get(self, request):
#         lat = request.query_params.get("lat")
#         lon = request.query_params.get("lon")
#         siti = request.query_params.get("siti_id")

#         distribution = Distribution(request.user.id, lon, lat)
#         resp = distribution.nearest_adresses(siti)

#         order_settings = OrderSettings.objects.first()
        
#         if not resp:
#             return Response({"status": True, "delivery_type": 2, "price": order_settings.people_price_delivery}) 

#         distance_m = distance_between_coordinates(float(lat), float(lon), resp.lat, resp.long)

#         if order_settings.people_long_delivery >= distance_m:
#             return Response({"status": True, "delivery_type": 1, "price": order_settings.people_price_delivery})
#         else:
#             return Response({"status": True, "delivery_type": 2, "price": order_settings.auto_price_delivery})


# class CheckMultiCart(APIView):
#     permission_classes = (IsAuthenticated, )

#     def get(self, request):
#         distribution = Distribution(request.user.id)
#         resp = distribution.check_true_order(request.query_params.get("siti_id"))

#         return Response(resp)


# class GetAdressForPickup(APIView):
#     permission_classes = (IsAuthenticated, )

#     def get(self, request):
#         cart = CartUser.objects.get(user=request.user.id)
#         if cart.products.count() != 0:
#             distribution = Distribution(request.user.id)
#             resp = distribution.check_true_order(request.query_params.get("siti_id"), get_adress=True)

#             list_id_adress = [i["market_id"] for i in resp["adress"]]
#             print(list_id_adress)

#             adress_id = request.query_params.get("adress_id")
#             if adress_id:
#                 adress = Adress.objects.get(pk=adress_id)
#                 nearest_delivery_point = find_nearest_addres(
#                     adress.long, 
#                     adress.lat, 
#                     is_list_adress=True, 
#                     list_id=list_id_adress, 
#                     siti_id=request.query_params.get("siti_id"))
                
#                 if nearest_delivery_point:
#                     image_shop = ImageShop.objects.filter(shop=nearest_delivery_point)
#                     data = {
#                         "id": nearest_delivery_point.pk, 
#                         "adress": nearest_delivery_point.adress, 
#                         "market": {
#                             "id": nearest_delivery_point.shop.pk,
#                             "name": nearest_delivery_point.shop.name,
#                             "short_description": nearest_delivery_point.shop.short_description,
#                             "description": nearest_delivery_point.shop.description,
#                             "link": nearest_delivery_point.shop.link,
#                         }, 
#                         "lat": nearest_delivery_point.long, 
#                         "long": nearest_delivery_point.lat,
#                         "is_around_clock": nearest_delivery_point.is_around_clock,

#                         "time": [
#                             [nearest_delivery_point.monday_with, nearest_delivery_point.monday_until],
#                             [nearest_delivery_point.tuesday_with, nearest_delivery_point.tuesday_until],
#                             [nearest_delivery_point.wednesday_with, nearest_delivery_point.wednesday_until],
#                             [nearest_delivery_point.thursday_with, nearest_delivery_point.thursday_until],
#                             [nearest_delivery_point.friday_with, nearest_delivery_point.friday_until],
#                             [nearest_delivery_point.saturday_with, nearest_delivery_point.saturday_until],
#                             [nearest_delivery_point.sunday_with, nearest_delivery_point.sunday_until],
#                         ],
#                         "phone": nearest_delivery_point.phone,
#                         "timeaone": f"{nearest_delivery_point.timezone}",
#                         "image": [f"/media/{i.image}" for i in image_shop],
#                     }
#                     resp["delivery_adress"] = data

#             return Response(resp)
#         else:
#             return Response({"status": False, "error": "cart_is_clear"})