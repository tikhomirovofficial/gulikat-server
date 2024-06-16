from django.urls import path, include

from settings.views import (
    GetErrorInClient,
    TestDistribution,
    GetOrderSettings,
    GetGlobalSettings,

    AdminMainView,
    AdminOrderView,
    AdminOrderInfo,
    AdminOrderChangeStatus,
)

urlpatterns = [
    path('error', GetErrorInClient.as_view(), name='GetErrorInClient'),
    path('distribution', TestDistribution.as_view(), name='TestDistribution'),
    path('order-settings', GetOrderSettings.as_view(), name='GetOrderSettings'),
    path('global', GetGlobalSettings.as_view(), name='GetGlobalSettings'),

    path('admin/main', AdminMainView.as_view(), name='admin_main_view'),
    path('admin/order', AdminOrderView.as_view(), name='AdminOrderView'),
    path('admin/order/<int:id>/', AdminOrderInfo.as_view(), name='AdminOrderInfo'),
    path('admin/order/<int:id>/change', AdminOrderChangeStatus.as_view(), name='AdminOrderChangeStatus'),
]