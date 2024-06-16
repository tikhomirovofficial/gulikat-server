from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from cart.models import (
    ProductsInCart,
    CartUser,
)

from market.models import (
    ProductsInAdress,
)

from product.models import (
    Products,
)

from settings.models import (
    AllProductsSettings,
)


class AddToCart(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = User.objects.get(pk=request.user.id)

        product_id = request.data["products_id"]
        count = request.data["count"]
        adress_id = request.data["adress_id"]

        cart_user, created = CartUser.objects.get_or_create(user=user)

        product_in_cart, created = ProductsInCart.objects.get_or_create(
            product_id=product_id,
            count=count
        )

        cart_user.products.add(product_in_cart)

        product = Products.objects.get(id=product_id)

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
            "count": count
        }

        total_price = 0.0
        total_price_discount = 0.0


        for product_in_cart in cart_user.products.all():
            product = product_in_cart.product
            discount_price = round(product.price * ((1 - (product.discount / 100) if product.discount != 0 else 1)), 2)
            total_price_discount += discount_price * product_in_cart.count
            total_price += product.price * product_in_cart.count


        return Response({"status": True, "cart_id": product_in_cart.pk, "product": product_data, "price": round(total_price, 2), "price_discount": round(total_price_discount, 2)}, status=status.HTTP_201_CREATED)


class ListCart(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        cart_user, created = CartUser.objects.get_or_create(user=user)
        if not cart_user:
            return Response({"status": False, "error": "cart_user_not_found"}, status=status.HTTP_404_NOT_FOUND)
        
        total_price = 0.0
        total_price_discount = 0.0

        cart_user_data = []

        adress_id = request.query_params.get("adress_id")

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
        
        return Response({"status": True, "cart": cart_user_data, "price": round(total_price, 2), "price_discount": round(total_price_discount, 2)})


class ClearCart(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        cart_user, created = CartUser.objects.get_or_create(user=user)
        cart_user.products.clear()

        return Response({"status": True})
            

class DeleteCart(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        cart_id = request.data["cart_id"]
        product_in_cart = ProductsInCart.objects.get(pk=cart_id)
        if product_in_cart:
            product_in_cart.delete()
            user = User.objects.get(pk=request.user.id)
            cart_user, created = CartUser.objects.get_or_create(user=user)
            if not cart_user:
                return Response({"status": False, "error": "cart_user_not_found"}, status=status.HTTP_404_NOT_FOUND)
        
            total_price = 0.0
            total_price_discount = 0.0

            adress_id = request.query_params.get("adress_id")

            cart_user_data = []

            for product_in_cart_v in cart_user.products.all():
                product = product_in_cart_v.product

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
                    "storeg_temperature": product.storeg_temperature,
                    "proteins": product.proteins,
                    "calories": product.calories,
                    "sheif_life": product.sheif_life,
                    "image": f"/media/{product.image}",
                    "is_activ": product.is_activ,
                    "count": product_in_cart.count
                }
                cart_user_data.append({
                    "id": product_in_cart_v.pk,
                    "product": product_data,
                    "count": product_in_cart.count
                    })

                total_price += product_data["price"] * product_in_cart_v.count
                total_price_discount += product_data["discount_price"] * product_in_cart_v.count
            return Response({"status": True, "cart": cart_user_data, "price": round(total_price, 2), "price_discount": round(total_price_discount, 2)})
        else:
            return Response({"status": False, "message": "cart_id not found"}, status=status.HTTP_404_NOT_FOUND)


class EditCountCart(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        cart_id = request.data["cart_id"]
        count = request.data["count"]
        product_in_cart = ProductsInCart.objects.filter(pk=cart_id).first()
        if product_in_cart:
            product = product_in_cart.product
            adress_id = request.data["adress_id"]

            product_in_adress = ProductsInAdress.objects.filter(adress=adress_id, products=product.pk).first()
            
            product_in_cart.count = count
            product_in_cart.save()
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
                "storeg_temperature": product.storeg_temperature,
                "sheif_life": product.sheif_life,
                "image": f"/media/{product.image}",
                "is_activ": product.is_activ,
                "count": product_in_adress.count
            }

            user = User.objects.get(pk=request.user.id)

            cart_user, created = CartUser.objects.get_or_create(user=user)

            total_price = 0.0
            total_price_discount = 0.0

            for product_in_cart in cart_user.products.all():
                product = product_in_cart.product
                discount_price = round(product.price * ((1 - (product.discount / 100) if product.discount != 0 else 1)), 2)
                total_price_discount += discount_price * product_in_cart.count
                total_price += product.price * product_in_cart.count


            return Response({"status": True, "cart_id": cart_id, "product": product_data, "count": count, "price": round(total_price, 2), "price_discount": round(total_price_discount, 2)})
        else:
            return Response({"status": False, "message": "cart_id not found"}, status=status.HTTP_404_NOT_FOUND )