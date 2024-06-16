from django.urls import path, include

from lk.views import (
    EditUser,
    AddAdress,
    GetAdress,
    DeleteAdress,
    GetUser,
)

urlpatterns = [
    path('', GetUser.as_view(), name='GetUser'),
    path('edit', EditUser.as_view(), name='EditUser'),
    path('adress/add', AddAdress.as_view(), name='AddAdress'),
    path('adress/get', GetAdress.as_view(), name='GetAdress'),
    path('adress/del', DeleteAdress.as_view(), name='DeleteAdress'),
]