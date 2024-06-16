from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from auth_main.tools.user_tools import (
    set_user_code,
    create_user,
    )


class UserCreateAuthCode(APIView):
    def post(self, request):
        username = request.data["phone"]
        user = User.objects.filter(username=username).first()
        if user:
            code = set_user_code(user)
            # user.set_password(code)
            return Response({"status": True})
        else:
            resp = create_user(username)
            return Response({"status": True}, status=status.HTTP_201_CREATED)
