from django.contrib import admin
from .models import User,UserActivity,UserFriends


admin.site.register(User)
admin.site.register(UserActivity)
admin.site.register(UserFriends)

