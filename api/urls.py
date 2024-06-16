from django.urls import path, include

urlpatterns = [
    path("auth/", include('auth_main.urls')),
    path("lk/", include('lk.urls')),
    path("market/", include('market.urls')),
    path("product/", include('product.urls')),
    path("cart/", include('cart.urls')),
    path("order/", include('order.urls')),
    path("settings/", include('settings.urls')),
    path("webhook/", include('webhook.urls')),
    # path("booking/", include('booking.urls')),
]