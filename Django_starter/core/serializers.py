from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import Towns, Regions, Agencies


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'groups']
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        # fields = ['url', 'name']
        fields = "__all__"


class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = "__all__"


class TownSerializer(serializers.ModelSerializer):
    name_region = serializers.ReadOnlyField()

    class Meta:
        model = Towns
        fields = "__all__"


class AgencySerializer(serializers.ModelSerializer):
    name_town = serializers.ReadOnlyField()

    class Meta:
        model = Agencies
        fields = "__all__"
