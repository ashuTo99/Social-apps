from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from .utils import generateToken
from .query import UserQuery,FriendQuery
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserActivity
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
        methods=['post'], 
        request_body=UserRegisterSerializer)
@api_view(['POST'])
def register(request):
    response = dict()
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response['status'] = 'success'
        response['message'] = "User created successfully"
        status_code = 201
    else:
        response['status'] = 'fail'
        response['message'] = serializer.errors
        status_code = 200
    return Response(response, status=status_code)


@swagger_auto_schema(
        methods=['post'], 
        request_body=UserLoginSerializer)
@api_view(['POST'])
def login(request):
    response = dict()
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        userObj = UserQuery.getUserByEmail(email)
        if userObj:
            token = generateToken('ACCESS_TOKEN',userObj)
            response['status'] = 'success'
            response['data'] = token
            response['message'] = "User logged in successfully "
            status_code = 200
        else:
            response['status'] = 'fail'
            response['data'] = {}
            response['message'] = "User not found"
            status_code = 200
    else:
        response['status'] = 'fail'
        response['message'] = serializer.errors
        status_code = 200
    return Response(response, status=status_code)

@swagger_auto_schema(
        methods=['get'], 
        responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def users(request):
    response = dict()
    userObjs = UserQuery.getUserList(request)
    serializer = UserSerializer(userObjs,many=True)
    response['status'] = 'success'
    response['data'] = serializer.data
    response['message'] = "User not found"
    status_code = 200

    return Response(response, status=status_code)


@swagger_auto_schema(
        methods=['post'], 
        request_body=SendRequestSerializer)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def sendFriendRequest(request):
    response = dict()
    senderObj = UserQuery.getUserById(int(request.user.id))
    serializer = SendRequestSerializer(data=request.data)
    if serializer.is_valid():
        friend_id = serializer.data['friend_id']
        receiverObj = UserQuery.getUserById(int(friend_id))
        activityObj = UserActivity.objects.filter(Q(sender_id=senderObj,receiver_id=receiverObj) | Q(sender_id=receiverObj,receiver_id=senderObj)).first()
        if not activityObj:
            can_send = FriendQuery.isCanSend(senderObj.id)
            if can_send:
                try :
                    activityObj = FriendQuery.saveFriendRequest(senderObj,receiverObj)
                    request_status = activityObj.request_status
                except Exception as e:
                    print('Error ==>',e)
                    request_status = None

                response['status'] = 'success'
                response['data'] = {'request_status':request_status}
                response['message'] = "Friend request sent success"
                status_code = 200
            else:
                response['status'] = 'success'
                response['data'] = {}
                response['message'] = "You can only send 3 request in a minute "
                status_code = 200
        else:
            response['status'] = 'success'
            response['data'] = {}
            response['message'] = "Friend request already sent"
            status_code = 200

    else:
        response['status'] = 'fail'
        response['message'] = serializer.errors
        status_code = 200

    return Response(response, status=status_code)

@swagger_auto_schema(
        methods=['get'], 
        responses={200: UserActivitySerializer(many=True)})
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def friendRequests(request):
    response = dict()
    userObjs = FriendQuery.getFriendRequests(int(request.user.id))
    serializer = UserActivitySerializer(userObjs,many=True)
    response['status'] = 'success'
    response['data'] = serializer.data
    response['message'] = "Data fetched successfully "
    status_code = 200
    return Response(response, status=status_code)


@swagger_auto_schema(
        methods=['post'], 
        request_body=FriendRequestSerializer)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def friendRequestStatus(request):
    response = dict()
    serializer = FriendRequestSerializer(data=request.data)
    if serializer.is_valid():
        status = serializer.data['status']
        request_id = serializer.data['request_id']
        requestObj = FriendQuery.getRequestById(int(request_id))
        if requestObj:
            is_friends = FriendQuery.isFriends(requestObj)
            if not is_friends:
                if status == "accepted":
                    requestObj.request_status = status
                    requestObj.save()
                    
                    try:
                        UserQuery.addFriend(requestObj)
                    except:
                        pass
                else:
                    requestObj.request_status = 'rejected'
                    requestObj.save()
                    
                response['status'] = 'success'
                response['data'] = {'request_status':requestObj.request_status}
                response['message'] = f"Friend request {requestObj.request_status} successfully"
                status_code = 200
            else:
                response['status'] = 'fail'
                response['data'] = {}
                response['message'] = "You are already friends"
                status_code = 200   
        else:
            response['status'] = 'fail'
            response['data'] = {}
            response['message'] = "Invalid request"
            status_code = 200   
    else:
        response['status'] = 'fail'
        response['data'] = {}
        response['message'] = serializer.errors
        status_code = 200

    return Response(response, status=status_code)


@swagger_auto_schema(
        methods=['get'], 
        responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def myFriends(request):
    response = dict()
    userObjs = FriendQuery.myFriends(int(request.user.id))
    serializer = UserSerializer(userObjs,many=True)
    response['status'] = 'success'
    response['data'] = serializer.data
    response['message'] = "Data fetched successfully "
    status_code = 200
    return Response(response, status=status_code)