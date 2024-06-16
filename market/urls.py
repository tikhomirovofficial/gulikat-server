from django.urls import path, include

from market.views import (
    GetSiti,
    GetNearestAdress,
    GetNearestAdressAndNotActivProduct,
#     GetMarketAdressInSiti,
#     GetMarketInfo,
#     FullInfoForAdress,
#     GetMarketInSiti,
)

urlpatterns = [
    path('', GetSiti.as_view(), name='GetSiti'),
    path('adress/nearest', GetNearestAdress.as_view(), name='GetNearestAdress'),
    path('adress/nearest/cart', GetNearestAdressAndNotActivProduct.as_view(), name='GetNearestAdressAndNotActivProduct'),
    # path('adress/siti', GetAdress.as_view(), name='GetAdress'),
    # path('adress/market/siti', GetMarketAdressInSiti.as_view(), name='GetMarketAdressInSiti'),
    # path('adress/info', FullInfoForAdress.as_view(), name='FullInfoForAdress'),
    # path('adress/market', GetMarketInSiti.as_view(), name='GetMarketInSiti'),
]