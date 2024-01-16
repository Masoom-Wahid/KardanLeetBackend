from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
)

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class MyTokenObtainSerializer(TokenObtainSerializer):
    default_error_messages = {
        "no_active_account": "invalid_credentials",
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, MyTokenObtainSerializer):
    pass


class MyTokenObtainPairSerializer(MyTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["is_superuser"] = user.is_superuser

        return token