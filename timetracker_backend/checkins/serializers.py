# checkins/serializers.py

from rest_framework import serializers
from .models import CheckIn
from django.contrib.auth.models import User
class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CheckInSerializerNew(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Serialize the user information

    class Meta:
        model = CheckIn
        fields = ['id', 'hours', 'tag', 'activities', 'user']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)