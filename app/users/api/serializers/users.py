from rest_framework import serializers
from users.models import Staff, User
from .userbase import UserBaseSerializer


class StaffSerializer(serializers.ModelSerializer):
    userbase_details = UserBaseSerializer(read_only=True, source='userbase')

    class Meta:
        model = Staff
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    userbase_details = UserBaseSerializer(read_only=True, source='userbase')

    class Meta:
        model = User
        fields = '__all__'
