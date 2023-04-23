from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Social App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ashuhardaska26@gmail.com"),
      
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register', views.register, name="api.register"),
    path('login', views.login, name="api.login"),
    path('users', views.users, name="api.users"),
    path('send-request', views.sendFriendRequest, name="api.send_request"),
    path('friend-requests', views.friendRequests, name="api.firend_request"),
    path('request-status', views.friendRequestStatus, name="api.request_status"),
    path('my-friends', views.myFriends, name="api.my-friends"),






    

]
