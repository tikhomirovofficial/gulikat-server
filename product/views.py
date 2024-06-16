from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from datetime import datetime
import re

from market.models import (
    Adress,
    ProductsInAdress,
)

from product.models import (
    Products,
    Category,
)

from settings.models import (
    AllProductsSettings,
)

class GetProductInAdress(APIView):
    def get(self, request):
        adress_id = request.query_params.get("adress_id")
        products = ProductsInAdress.objects.filter(adress=adress_id)

        products_data = [
            {
                "id": product.products.pk,
                "category": {
                    "id": product.products.category.pk,
                    "title": product.products.category.title
                    },
                "title": product.products.title,
                "description": product.products.description,
                "price": product.products.price,
                "discount_price": round(product.products.price * ((1 - (product.products.discount / 100) if product.products.discount != 0 else 1)), 2),
                "discount_procent": product.products.discount,
                "weight": product.products.weight,
                "dimensions": {
                    "id": product.products.dimensions.pk,
                    "title": product.products.dimensions.title
                    },
                "fats": product.products.fats,
                "proteins": product.products.proteins,
                "calories": product.products.calories,
                "carbohydrates": product.products.carbohydrates,
                "storeg_temperature": product.products.storeg_temperature,
                "sheif_life": product.products.sheif_life,
                "image": f"/media/{product.products.image}",
                "is_activ": product.products.is_activ,
                "count": product.count,

            } for product in products
        ]

        return Response({"status": True, "products": products_data})


class GetCategoryInAdress(APIView):
    def get(self, request):
        adress_id = request.query_params.get("adress_id")
        products = ProductsInAdress.objects.filter(adress=adress_id)

        products_data = [
            {
                "id": product.products.category.pk,
                "title": product.products.category.title
            } for product in products
        ]
        unique_ids = {}

        # Фильтруем данные, оставляя только уникальные значения по полю id
        unique_data = [unique_ids.setdefault(item["id"], item) for item in products_data if item["id"] not in unique_ids]


        return Response({"status": True, "category": unique_data})


class GetProductInAdressDiscount(APIView):
    def get(self, request):
        adress_id = request.query_params.get("adress_id")
        products = ProductsInAdress.objects.filter(adress=adress_id)

        products_data = [
            {
                "id": product.products.pk,
                "category": {
                    "id": product.products.category.pk,
                    "title": product.products.category.title
                    },
                "title": product.products.title,
                "description": product.products.description,
                "price": product.products.price,
                "discount_price": round(product.products.price * ((1 - (product.products.discount / 100) if product.products.discount != 0 else 1)), 2),
                "discount_procent": product.products.discount,
                "weight": product.products.weight,
                "dimensions": {
                    "id": product.products.dimensions.pk,
                    "title": product.products.dimensions.title
                    },
                "fats": product.products.fats,
                "proteins": product.products.proteins,
                "calories": product.products.calories,
                "carbohydrates": product.products.carbohydrates,
                "storeg_temperature": product.products.storeg_temperature,
                "sheif_life": product.products.sheif_life,
                "image": f"/media/{product.products.image}",
                "is_activ": product.products.is_activ,
                "count": product.count,

            } for product in products if product.products.discount != 0
        ]

        return Response({"status": True, "products": products_data})