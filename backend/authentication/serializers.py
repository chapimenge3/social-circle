from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "image",
            "bio",
            "birth_date",
            "location",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "email", "username", "created_at", "updated_at")