from .models import User,UserActivity,UserFriends
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, timedelta


class UserQuery:
    def __init__(self):
        pass

    def getUserById(id:int):
        try:
            userObj = User.objects.filter(id=id).first()
        except:
            userObj = None
        return userObj

    def getUserByEmail(email):
        try:
            userObj = User.objects.filter(email__iexact=email).first()
        except:
            userObj = None
        return userObj
    
    def getUserList(request):
        user_id = request.user.id
        page = request.GET.get('page',1)
        search = request.query_params.get('search','')
        page_size = request.query_params.get('page_size',1)

        userObjs = User.objects.filter(is_active=True,is_superuser=False).exclude(id=user_id)
        if search:
            userObjs = userObjs.filter(Q(email__contains=search)|Q(full_name__contains=search))
        
        if page_size and page:
            paginator = Paginator(userObjs, page_size)  
            try:
                userObjs = paginator.page(page)
            except PageNotAnInteger:
                userObjs = paginator.page(1)
            except EmptyPage:
                userObjs = paginator.page(paginator.num_pages)

        return userObjs
    



class FriendQuery:
    def __init__(self):
        pass

    def saveFriendRequest(sender,receiver):
        userActivityObj = None
        if sender and receiver:
            userActivityObj = UserActivity()
            userActivityObj.sender_id = sender
            userActivityObj.receiver_id = receiver
            userActivityObj.request_status = 'pending'
            userActivityObj.save()
        return userActivityObj
    

    def isCanSend(sender_id:int):
        time_to = datetime.now() 
        time_from = time_to - timedelta(minutes=1)
        requestCount = UserActivity.objects.filter(sender_id__id=sender_id,sent_on__range=[time_from,time_to]).count()
        if requestCount == 3 :
            status = False
        else:
            status = True
        return status

    def getRequestById(id:int):
        obj = UserActivity.objects.filter(id=id).first()
        return obj

    def getFriendRequests(receiver_id:int):
        requests = UserActivity.objects.filter(receiver_id__id=receiver_id,request_status='pending')    
        return requests
    
    def addFriend(requestObj):
        fiendObj = UserFriends()
        fiendObj.user_id = requestObj.receiver_id
        fiendObj.friend_id = requestObj.sender_id
        fiendObj.save()

    def isFriends(requestObj):
        status = False
        friendObj = UserFriends.objects.filter(Q(user_id=requestObj.receiver_id,friend_id = requestObj.sender_id) |
                                               Q(user_id=requestObj.sender_id,friend_id = requestObj.receiver_id)).first()
        if friendObj:
            status = True
        return status
    
    def myFriends(id:int):
        friendObjs = UserFriends.objects.filter(Q(user_id__id=id) | Q(friend_id__id=id))
        user_ids = friendObjs.values_list('user_id__id',flat=True).distinct()
        friend_ids = friendObjs.values_list('friend_id__id',flat=True).distinct()
        all_ids = list(set(user_ids) | set(friend_ids))
        userObjs = User.objects.filter(id__in =all_ids).exclude(id=id)
        return userObjs





    
    