from django.contrib import admin
from order.models import (
    UserOrderHystory,
    StatusDelivery,
)

admin.site.register(UserOrderHystory)
admin.site.register(StatusDelivery)