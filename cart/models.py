from django.db import models
from django.contrib.auth.models import User

from product.models import (
    Products,
)


class ProductsInCart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Продукт")
    count = models.IntegerField(verbose_name="Количество")

    def __str__(self) -> str:
        return f'{self.product}'
    
    class Meta:
        verbose_name_plural = 'Продукты в корзине'


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(ProductsInCart, verbose_name="Продукты")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'
    
    class Meta:
        verbose_name_plural = 'Корзины'