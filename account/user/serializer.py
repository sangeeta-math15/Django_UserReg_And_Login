from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    """
    Serializer is used to converting the json data
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(max_length=254)
    is_verified = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.create_user(**validated_data)
