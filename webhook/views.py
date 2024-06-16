from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# from settings.tools.telegram import (
#     # send_message_order,
#     TelegramBot
# )


# from order.models import (
#     UserOrderHystory
# )

# class AddPayment(APIView):
#     def post(self, request):
#         if request.data["object"]["status"] == "succeeded":
#             uoh = UserOrderHystory.objects.filter(pyment_id=request.data["object"]["id"]).first()
#             if uoh:
#                 uoh.is_pyment = True
#                 uoh.save()
#                 th = TelegramBot(uoh.pk)
#                 th.start()
#         return Response({})