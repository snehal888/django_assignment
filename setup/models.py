from django.db import models
from .validations import *
from django.utils import timezone

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class User(models.Model):
    name               = models.CharField(max_length=230, null=True, validators=[is_valid_string])
    email              = models.CharField(max_length=230, null=True, unique=True,validators=[is_valid_string])
    password           = models.CharField(max_length=230, null=True, validators=[is_valid_password])
    created_at         = models.DateTimeField(default=timezone.now)
    updated_at         = AutoDateTimeField(default=timezone.now)
 
class FriendRequest(models.Model):
    from_user          = models.ForeignKey(User,on_delete=models.CASCADE, max_length=100,null=False,blank=False, related_name='from_user')
    to_user            = models.ForeignKey(User,on_delete=models.CASCADE, max_length=100,null=False,blank=False, related_name='to_user')
    timestamp          = models.CharField(max_length=230, null=True, validators=[is_valid_timestamp])
    status             = models.CharField(max_length=230, null=True, validators=[is_valid_password], default='send')
    created_at         = models.DateTimeField(default=timezone.now)
    updated_at         = AutoDateTimeField(default=timezone.now)





