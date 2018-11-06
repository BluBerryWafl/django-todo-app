from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework import serializers
from base import models


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToDo
        fields = ("id", "text", "user", "done")
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated is False:
            raise PermissionDenied
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")
        read_only_fields = ("id", "username")


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=200)
