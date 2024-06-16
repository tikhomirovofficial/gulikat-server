from django.urls import path, include

from cart.views import (
    AddToCart,
    ListCart,
    DeleteCart,
    EditCountCart,
    # UpdateSupplementsInCart,
    # AddCombo,
    # DeleteCombo,
    # UpdateComboInCart,
    ClearCart,
)

urlpatterns = [
    path('add', AddToCart.as_view(), name='AddToCart'),
    # path('add/combo', AddCombo.as_view(), name='AddCombo'),
    path('list', ListCart.as_view(), name='ListCart'),
    path('clear', ClearCart.as_view(), name='ClearCart'),
    path('edit', EditCountCart.as_view(), name='EditCountCart'),
    # path('edit/combo', UpdateComboInCart.as_view(), name='UpdateComboInCart'),
    path('delete', DeleteCart.as_view(), name='DeleteCart'),
    # path('delete/combo', DeleteCombo.as_view(), name='DeleteCombo'),
    # path('edit/supplements', UpdateSupplementsInCart.as_view(), name='UpdateSupplementsInCart'),
]