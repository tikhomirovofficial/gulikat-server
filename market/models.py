from django.db import models
import uuid
from datetime import datetime

from product.models import (
    Products,
)


class Siti(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название города")
    
    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Города'


class Adress(models.Model):
    title = models.CharField(max_length=500, verbose_name="Адрес")
    siti = models.ForeignKey(Siti, on_delete=models.CASCADE, verbose_name="Город")
    long = models.FloatField(default=0.0, verbose_name="Долгота")
    lat = models.FloatField(default=0.0, verbose_name="Широта")
    is_main_for_siti = models.BooleanField(default=False, verbose_name="Основной для города?")
    is_activ = models.BooleanField(default=True, verbose_name="Активен?")

    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Адреса магазинов'


class ProductsInAdress(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Продукт")
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE, verbose_name="Адрес")
    count = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self) -> str:
        return f'{self.products}'
    
    class Meta:
        verbose_name_plural = 'Продукты в адресах'