import json

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """Profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    contacts = models.CharField(max_length=255, blank=True, null=True)
    edit_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    """Model to insert notes"""
    note = models.CharField(max_length=255)


class WebRequest(models.Model):
    """Model for saving requests"""
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    status_code = models.IntegerField()
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.GenericIPAddressField()
    remote_addr_fwd = models.GenericIPAddressField(blank=True, null=True)
    meta = models.TextField()
    cookies = models.TextField(blank=True, null=True)
    get = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    raw_post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)


def dumps(value):
    return json.dumps(value, default=lambda o: None)
