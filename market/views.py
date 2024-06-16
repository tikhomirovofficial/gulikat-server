from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from market.models import (
    Siti,
    Adress,
    ProductsInAdress,
)

from lk.models import Adress as UserAdress

from market.tools.geo import find_nearest_addres

from product.models import Products

from cart.models import CartUser


class GetSiti(APIView):
    def get(self, request):
        siti = []

        for i in Siti.objects.all():
            base_adress = Adress.objects.filter(siti=i.pk, is_main_for_siti=True).first()
            siti.append({
                "id": i.pk, 
                "name": i.title,
                "base_adress_id": (base_adress.pk if base_adress else 0)
            })
        return Response({"status": True, "siti": siti})


class GetNearestAdress(APIView):
    def get(self, request):
        user_adress_id = request.query_params.get("user_adress_id")
        siti_id = request.query_params.get("siti_id")
        user_adress = UserAdress.objects.get(pk=user_adress_id)

        adress_market = find_nearest_addres(user_adress.long, user_adress.lat, siti_id)
        if isinstance(adress_market, Adress):
            return Response({"status": True, "adress": adress_market.pk})
        else:
            return Response({"status": False})


class GetNearestAdressAndNotActivProduct(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_adress_id = request.query_params.get("user_adress_id")
        siti_id = request.query_params.get("siti_id")
        user_adress = UserAdress.objects.get(pk=user_adress_id)

        adress_market = find_nearest_addres(user_adress.long, user_adress.lat, siti_id)
        if isinstance(adress_market, Adress):
            user = User.objects.get(pk=request.user.id)
            cart_user, created = CartUser.objects.get_or_create(user=user)

            id_products_in_cart = [i.product.pk for i in cart_user.products.all()]

            print(id_products_in_cart)

            products_in_adress = ProductsInAdress.objects.filter(adress = adress_market.pk, products__in=id_products_in_cart)

            not_activ_products = []
            for product_in_adress in products_in_adress:
                if product_in_adress.count == 0 or product_in_adress.products.is_activ == False:
                    not_activ_products.append(product_in_adress)
            
            products_data = [
                {
                    "id": product_in_adress.products.pk,
                    "category": {
                        "id": product_in_adress.products.category.pk,
                        "title": product_in_adress.products.category.title
                        },
                    "title": product_in_adress.products.title,
                    "description": product_in_adress.products.description,
                    "price": product_in_adress.products.price,
                    "discount_price": round(product_in_adress.products.price * ((1 - (product_in_adress.products.discount / 100) if product_in_adress.products.discount != 0 else 1)), 2),
                    "discount_procent": product_in_adress.products.discount,
                    "weight": product_in_adress.products.weight,
                    "dimensions": {
                        "id": product_in_adress.products.dimensions.pk,
                        "title": product_in_adress.products.dimensions.title
                        },
                    "fats": product_in_adress.products.fats,
                    "carbohydrates": product_in_adress.products.carbohydrates,
                    "storeg_temperature": product_in_adress.products.storeg_temperature,
                    "sheif_life": product_in_adress.products.sheif_life,
                    "image": f"/media/{product_in_adress.products.image}",
                    "is_activ": product_in_adress.products.is_activ,
                    "count": product_in_adress.count
                } for product_in_adress in not_activ_products
            ]

            return Response({"status": True, "products": products_data, "adress": adress_market.pk})
        else:
            return Response({"status": False, "error": "nearest_adress_not_found"})
        

        


# @tiksoft_official Вопрос, вариант если я буду отдавать тебе не недоступные товары в корзине, а наоборот доступные?