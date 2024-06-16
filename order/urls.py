from django.urls import path, include

from order.views import (
    CreateOrder,
    GetOrder,
    ListOrder,
#     OrderPaymentSuccess,
#     GetDeliveryType,
#     GetPaymentType,
#     GetTypeDeliveryForCoord,
#     CheckMultiCart,
#     GetAdressForPickup,
)

urlpatterns = [
    path('create', CreateOrder.as_view(), name='CreateOrder'),
    path('get', GetOrder.as_view(), name='GetOrder'),
    path('list', ListOrder.as_view(), name='ListOrder'),
    # path('success', OrderPaymentSuccess.as_view(), name='OrderPaymentSuccess'),
    # path('delivery/list', GetDeliveryType.as_view(), name='GetDeliveryType'),
    # path('payment/list', GetPaymentType.as_view(), name='GetPaymentType'),
    # path('geo/delivery/type', GetTypeDeliveryForCoord.as_view(), name='GetTypeDeliveryForCoord'),
    # path('check', CheckMultiCart.as_view(), name='CheckMultiCart'),
    # path('check/get-adress', GetAdressForPickup.as_view(), name='GetAdressForPickup'),
]