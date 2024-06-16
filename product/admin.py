from django import forms
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from product.models import (
    Category,
    Products,
    Dimensions,
)



class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'weight')  # Перечислите поля, которые вы хотите отображать в списке товаров
    list_filter = ('category',)  # Добавьте фильтр по категории
    search_fields = ('title',)  # Добавьте поле для поиска по названию товара
    ordering = ('category', 'title')  # Установите порядок сортировки
    

admin.site.register(Products, ProductsAdmin)
admin.site.register(Category)
admin.site.register(Dimensions)
