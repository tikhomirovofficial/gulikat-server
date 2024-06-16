from django.contrib import admin
from cart.models import (
    ProductsInCart,
    CartUser,
)


admin.site.register(ProductsInCart)
admin.site.register(CartUser)