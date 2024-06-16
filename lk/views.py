from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from lk.models import Profile, Adress

from lk.tools.geo import Geo


class EditUser(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        email = request.data["email"]
        dob = request.data["dob"]
        name = request.data["name"]

        user = User.objects.filter(pk=request.user.id).first()
        user.email = email
        user.first_name = name

        user.profile.dob = dob
        user.save()
        user.profile.save()
        user_data = {
            "id": user.pk,
            "phone": user.username,
            "email": user.email,
            "name": user.first_name,
            "dob": (user.profile.dob if user.profile.dob else "")
        }
        return Response({"status": True, "user": user_data})


class AddAdress(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # geo = Geo(request.data["adress"])
        
        adress = Adress.objects.create(
            adress = request.data["adress"],
            long = request.data["long"],
            lat = request.data["lat"],
            entrance = request.data["entrance"],
            floor = request.data["floor"],
            door_code = request.data["door_code"],
            apartment = request.data["apartment"],
        )

        user = User.objects.filter(pk=request.user.id).first()
        user.profile.adress.add(adress)
        user.profile.save()
        return Response({"status": True, "id": adress.pk}, status=status.HTTP_201_CREATED)


class DeleteAdress(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        adress_id = request.data["adress_id"]
        user = User.objects.get(pk=request.user.id)
        adress = Adress.objects.get(pk=adress_id)
        user.profile.adress.remove(adress)
        return Response({"status": True})


class GetAdress(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.filter(pk=request.user.id).first()
        adress = [{
            "id": i[0], 
            "adress": i[1], 
            "entrance": i[2], 
            "floor": i[3], 
            "door_code": i[4],
            "apartment": i[5],
            "long": i[6],
            "lat": i[7],
            } for i in user.profile.adress.values_list()]        
        return Response({"status": True, "adress": adress})


class GetUser(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.filter(pk=request.user.id).first()
        userdata = {
            "name": user.first_name,
            "email": user.email,
            "phone": user.username,
            "dob": (user.profile.dob if user.profile.dob else "")
        }
        return Response({"status": True, "user": userdata})


