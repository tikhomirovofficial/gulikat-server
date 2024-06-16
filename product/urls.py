from django.urls import path, include

from product.views import (
    GetProductInAdress,
    GetCategoryInAdress,
    GetProductInAdressDiscount,
#     GetComboForMarket,
#     GetProductDayForMarket,
#     GetSupplementsForId,
#     GetSouse,
)

urlpatterns = [
    path('in-market', GetProductInAdress.as_view(), name='GetProductInAdress'),
    path('category', GetCategoryInAdress.as_view(), name='GetCategoryInAdress'),
    path('in-market/discount', GetProductInAdressDiscount.as_view(), name='GetProductInAdressDiscount'),
    # path('combo', GetComboForMarket.as_view(), name='GetComboForMarket'),
    # path('day', GetProductDayForMarket.as_view(), name='GetProductDayForMarket'),
    # path('supplements', GetSupplementsForId.as_view(), name='GetSupplementsForId'),
    # path('souse', GetSouse.as_view(), name='GetSouse'),
]