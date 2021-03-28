import os

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from core.serializers import *

from rest_framework import generics, status, request
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
import csv



# ===================================  WEB Views ===================================

def home(request):
    return render(request, 'home/home.html')


def page1(request):
    return render(request, 'pages/page1.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home/home.html')


@login_required
def get_this_town(request, pk):
    town = get_object_or_404(Towns, pk=pk)
    return render(request, 'pages/town.html', {"town": town})


# ===================================  API Views ===================================

def check_token(self, request):
    # token = request.data.get("token")
    token_test = get_object_or_404(Token, key=request)
    if token_test:
        return True
    else:
        return False


class UsersView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get("token")
        # print(token)

        if get_object_or_404(Token, key=token):
            # print('hey 1')
            users = User.objects.all().order_by('-date_joined')
            serializer = UserSerializer(users, many=True)
            return Response({"users": serializer.data})


class GroupsView(APIView):
    def put(self, request):
        token = request.data.get("token")
        # print(token)
        if get_object_or_404(Token, key=token):
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)
            return Response({"groups": serializer.data})


class LogoutView(APIView):
    def post(self, request):
        token = request.data.get("token")
        # print(token)
        if get_object_or_404(Token, key=token):
            logout(request)
            return Response({"Respond": "Logout"})


class TownsView(APIView):
    def post(self, request):
        token = request.data.get("token")
        # print(token)
        if get_object_or_404(Token, key=token):
            towns = Towns.objects.all()
            serializer = TownSerializer(towns, many=True)
            return Response({"towns": serializer.data})


class GetAgence(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            agence = Agencies.objects.all().order_by('id')
            serializer = AgencySerializer(agence, many=True)
            return Response({"agence": serializer.data})


class AddRegion(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            serializer = RegionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"saved"})
            else:
                return Response({"Invalid Serializer"})
        else:
            return Response({"Not saved"})


class GetRegions(APIView):
    def post(self, request):
        token = request.data.get("token")
        # print(token)
        if get_object_or_404(Token, key=token):
            regions = Regions.objects.all()
            serializer = RegionsSerializer(regions, many=True)
            return Response({"regions": serializer.data})


class UpdateRegion(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            region = get_object_or_404(Regions, id=request.data.get("id"))
            region.region = request.data.get("region")
            region.code = request.data.get("code")
            region.save()
            region = get_object_or_404(Regions, id=request.data.get("id"))
            serializer = RegionsSerializer(region)
            return Response({"region": serializer.data})


class AddTown(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            region = get_object_or_404(Regions, id=request.data.get("region"))
            town = Towns()
            town.town = request.data.get("town")
            town.region = region
            town.code = request.data.get("code")
            town.save()
            serializer = TownSerializer(town)
            return Response({"town": serializer.data})
        else:
            return Response({"Unauthorized"})


class UpdateTown(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            town = get_object_or_404(Towns, id=request.data.get("id"))
            town.region = get_object_or_404(Regions, id=request.data.get("region"))
            town.town = request.data.get("town")
            town.code = request.data.get("code")
            town.save()
            return Response({"Updated"})


class AddAgence(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            town = get_object_or_404(Towns, id=request.data.get("town"))
            agence = Agencies()
            agence.town = town
            agence.agency = request.data.get("agency")
            agence.code = request.data.get("code")
            agence.email = request.data.get("email")
            agence.address = request.data.get("address")
            agence.telephone = request.data.get("telephone")
            agence.save()
            serializer = AgencySerializer(agence)
            return Response({"Agence": serializer.data})
        else:
            return Response({"Unauthorized"})


class UpdateAgence(APIView):
    def post(self, request):
        if get_object_or_404(Token, key=request.data.get("token")):
            agence = get_object_or_404(Agencies, id=request.data.get("id"))
            if agence:
                town = get_object_or_404(Towns, id=request.data.get("town"))
                agence.town = town
                agence.agency = request.data.get("agency")
                agence.code = request.data.get("code")
                agence.email = request.data.get("email")
                agence.address = request.data.get("address")
                agence.telephone = request.data.get("telephone")
                agence.save()
                serializer = AgencySerializer(agence)
                return Response({"Agence": serializer.data})
            else:
                return Response({"Agency Unknown"})
        else:
            return Response({"Unauthorized"})


class CSVManipulation(APIView):
    def post(self, request):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'CSVFiles')
        file_to_open = os.path.join(file_path, 'real_estate_price_size.csv')
        with open(file_to_open, 'r') as csv_file:
            csv_handler = csv.reader(csv_file)

            with open('new_prices.csv', 'w') as new_csv_file:
                writing_csv = csv.writer(new_csv_file, delimiter=',')

                for line in csv_handler:
                        writing_csv.writerow(line)
        return Response({"READ File Successfully"})



class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class LoginView(APIView):
    def post(self, request):
        data = dict()
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        urs = get_object_or_404(User, pk=token.user_id)
        # JsonResponse(data)
        return Response(
            {"token": token.key, "user_id": token.user_id, "Username": urs.username, "Name": urs.get_full_name(),
             # "birthDate": urs.staff.birthDate,
             # "role": urs.student.role, "department": urs.student.department.department_name,
             # "matriculation": urs.staff.matriculation,
             # "program": urs.student.degree_programm, "nationality": urs.student.nationality,
             # "picture": urs.staff.picture.url,
             # "phone": urs.staff.telephone, "address": urs.staff.address,
             # "birthPlace": urs.staff.birthPlace,
             # "marital_status": urs.staff.marital_status,
             # "gender": urs.staff.gender,
             # "region": urs.student.region, "admited_on": urs.date_joined,
             "email": urs.email,
             # "branch": urs.staff.agence.agence,
             # "branch_email": urs.staff.agence.email,
             # "branch_address": urs.staff.agence.address,
             # "branch_telephone": urs.staff.agence.telephone,
             # "profil": urs.staff.profil.name,
             # "profil_id": urs.staff.profil.id,
             "last_login": urs.last_login.strftime("%H:%M:%S  | %d - %m - %Y| GMT +1"),
             "date_joined": urs.date_joined.strftime("%H:%M:%S  | %d - %m - %Y| GMT +1"),
             })
        # {"token": token.key, "user_id": token.user_id, "Username": urs.username, "Name": urs.get_full_name(),
        #  "picture": urs.profile.picture.url, "Role": urs.profile.role}
