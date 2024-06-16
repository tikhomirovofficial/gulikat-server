from django.contrib import admin

from settings.models import (
    OrderSettings,
    ErrorClient,
    AllProductsSettings,
    GlobalSettings,
)

admin.site.site_header = "Гуликат"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Администрирование Гуликат"

admin.site.register(OrderSettings)
admin.site.register(ErrorClient)
admin.site.register(AllProductsSettings)
admin.site.register(GlobalSettings)