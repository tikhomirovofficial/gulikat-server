from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from settings.models import (
    ErrorClient,
)

from order.models import UserOrderHystory, StatusDelivery

from settings.models import (
    OrderSettings,
    GlobalSettings,
)

from market.models import (
    Siti,
    Adress,
)

from settings.tools.distribution import Distribution

class GetErrorInClient(APIView):
    def post(self, request):
        datetime = request.data["datetime"]
        sent_data = request.data["sent_data"]
        received_response = request.data["received_response"]
        status = request.data["status"]
        user = request.data["user"]
        url = request.data["url"]

        error_client = ErrorClient.objects.create(
            datetime=datetime,
            sent_data=sent_data,
            received_response=received_response,
            status=status,
            user=user,
            url=url
        )
        
        return Response({"status": True})


class TestDistribution(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        distribution = Distribution(request.user.id)

        return Response(distribution.check_multi_shop())


class GetOrderSettings(APIView):
    def get(self, request):
        order_settings = OrderSettings.objects.last()

        data = {
            "status": True,
            "car_min": order_settings.min_prise_auto,
            "people_min": order_settings.people_price_delivery

        }

        return Response(data)


class GetGlobalSettings(APIView):
    def get(self, request):
        gs = GlobalSettings.objects.last()
        data = {
            "is_dev": gs.is_dev,
            "is_disabled_cart": gs.is_disabled_cart,
            "is_disabled_online_pyment": gs.is_disabled_online_pyment,
            "is_disabled_cash_pyment": gs.is_disabled_cash_pyment,
            "is_disabled_auto_delivery": gs.is_disabled_auto_delivery,
            "is_disabled_people_delivery": gs.is_disabled_people_delivery,
            "is_disabled_pickup_delivery": gs.is_disabled_pickup_delivery,
            "is_disabled_reservation": gs.is_disabled_reservation,
            "is_disabled_order": gs.is_disabled_order
        }

        return Response(data)


def is_admin_user(user):
    return user.is_authenticated and user.is_staff

@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class AdminMainView(View):

    def get(self, request):
        # if request.user.is_authenticated:
        sitis = [{
            "id": i.pk,
            "title": i.title
        } for i in Siti.objects.all()]

        context = {
            "sitis": sitis
        }
        return render(request, "settings/admin_main.html", context=context)
        # else:
            # return redirect("/admin/login/?next=/admin/login")


@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class AdminOrderView(View):
    permission_classes = (IsAuthenticated, IsAdminUser, )

    def get(self, request):
        siti_id = self.request.GET.get("city")
        sitis = [{
            "id": i.pk,
            "title": i.title
        } for i in Siti.objects.all()
        ]

        adresses = [i.pk for i in Adress.objects.filter(siti=int(siti_id))]

        status_color = {
            "Создано": "bg-danger",
            "Принято": "bg-warning",
            "В сборке": "bg-info",
            "В доставке": "bg-primary",
            "Доставлено": "bg-success"
        }

        orders = [
            {
                "id": i.pk,
                "price": i.price,
                "datetime": i.datetime,
                "user": i.user,
                "status": i.status,
                "status_color": status_color[i.status.title],
            } for i in UserOrderHystory.objects.filter(market_adress__in=adresses).order_by("-datetime") if i.is_pyment
        ]

        context = {
            "sitis": sitis,
            "orders": orders
        }
        return render(request, "settings/admin_order.html", context=context)


@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class AdminOrderInfo(View):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    def get(self, request, id):
        sitis = [{
            "id": i.pk,
            "title": i.title
        } for i in Siti.objects.all()
        ]

        status_color = {
            "Создано": "bg-danger",
            "Принято": "bg-warning",
            "В сборке": "bg-info",
            "В доставке": "bg-primary",
            "Доставлено": "bg-success"
        }

        user_order = UserOrderHystory.objects.get(pk=id)

        if user_order.status.pk != 5:
            next_status = StatusDelivery.objects.get(id=user_order.status.pk+1)
        else:
            next_status = None

        order_data = {
            "id": user_order.pk,
            "user": user_order.user,
            "datetime": user_order.datetime,
            "price": int(user_order.price),
            "is_payment": user_order.is_pyment,
            "payment_url": f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={user_order.pyment_id}",
            "status": {
                "id": user_order.status.pk,
                "title": user_order.status.title,
                "color": status_color[user_order.status.title],
                "is_next": (True if next_status else False),
                "next_url": f"/api/settings/admin/order/{user_order.pk}/change?next={next_status.pk if next_status else None}",
                "next_title": (next_status.title if next_status else None),
                "next_id": (next_status.pk if next_status else None),
                "next_color": (status_color[next_status.title] if next_status else None)
                },
            "products": [{
                "id": product.id,
                "price": product.product.price,
                "discount_price": round(product.product.price * ((1 - (product.product.discount / 100) if product.product.discount != 0 else 1)), 2),
                "discount_procent": product.product.discount,
                "title": product.product.title,
                "image": f"/media/{product.product.image}",
                "count": product.count,
                } for product in user_order.products.all()],
            "adress": str(user_order.user_adress),
        }

        if user_order.status.pk == 1:
            next = {
                "id": 2,
                "title": "Принято"
                }
        elif user_order.status.pk == 2:
            next = {
                "id": 3,
                "title": "В сборке"
                }
        elif user_order.status.pk == 3:
            next = {
                "id": 4,
                "title": "В доставке"
                }
        elif user_order.status.pk == 4:
            next = {
                "id": 5,
                "title": "Доставлено"
                }
        else:
            next = {
                "id": 0
            }
        
        context = {
            "sitis": sitis,
            "order": order_data,
            "next": next
        }
        return render(request, "settings/admin_order_info.html", context=context)


@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class AdminOrderChangeStatus(View):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    def get(self, request, id):
        sitis = [{
            "id": i.pk,
            "title": i.title
        } for i in Siti.objects.all()
        ]

        user_order = UserOrderHystory.objects.get(pk=id)
        user_order.status = StatusDelivery.objects.get(id=int(self.request.GET.get("next")))
        user_order.save()

        
        context = {
            "sitis": sitis,
        }

        return redirect(f"/api/settings/admin/order/{id}")
        # return render(request, "settings/admin_order_info.html", context=context)