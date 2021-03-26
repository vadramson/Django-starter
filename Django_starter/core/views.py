from django.contrib.auth.decorators import login_required
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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


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
