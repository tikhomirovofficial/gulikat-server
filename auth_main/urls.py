from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from auth_main.views import UserCreateAuthCode

app_name = 'auth_main'

urlpatterns = [
    path('token/get', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/create', UserCreateAuthCode.as_view(), name='UserCreateAuthCode'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    ]