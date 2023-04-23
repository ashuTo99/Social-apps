from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email address is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)


        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_staff') is not True:
                raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(email, password, **extra_fields)
    



class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=200,blank=True,null=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        self.password= make_password(self.password)
        super(User, self).save(*args, **kwargs)


    def has_perm(self, perm, obj=None):
       return self.is_superuser
    
    def has_module_perms(self, app_label):
           return self.is_superuser
    
class UserActivity(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')]
    sender_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    request_status = models.CharField(max_length=100,choices=STATUS_CHOICES,default='pending')
    sent_on = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.request_status)


class UserFriends(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    friend_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user_id.email)