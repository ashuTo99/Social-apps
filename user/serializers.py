from rest_framework import serializers, exceptions
from .models import User,UserActivity,UserFriends


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','full_name']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','email','full_name','is_active']

    
class SendRequestSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField(required=True)


class FriendRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField(required=True)
    status = serializers.CharField(required=True)

    

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id','sender_id','receiver_id','request_status']


