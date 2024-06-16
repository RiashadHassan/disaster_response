from rest_framework import serializers

from core.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "slug", "email", "first_name", "last_name"]
        read_only_fields = fields


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "slug", "email", "first_name", "last_name"]
        read_only_fields = fields
