from django.contrib import admin
from market.models import (
    Adress,
    Siti,
    ProductsInAdress
)

class ProductsInAdressAdmin(admin.ModelAdmin):
    list_display = ('products', 'adress', 'count',)  # Перечислите поля, которые вы хотите отображать в списке товаров
    list_filter = ('adress',)  # Добавьте фильтр по категории
    search_fields = ('products__title',)  # Добавьте поле для поиска по названию товара
    ordering = ('products', 'adress', 'count',)  # Установите порядок сортировки

admin.site.register(Adress)
admin.site.register(Siti)
admin.site.register(ProductsInAdress, ProductsInAdressAdmin)
