from django.db import models
from django.contrib.auth.models import User
import uuid


User._meta.get_field('email')._unique = True

class UserLoginDetails(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    user_ip_address = models.CharField(max_length=100)
    os_details = models.CharField(max_length=100)
    browser_details = models.CharField(max_length=100)
    status = models.IntegerField(blank=True, null=True)
    attempt = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user, self.user_ip_address)

    class Meta:
        ordering = ['created_at']

class UserVerificationStatus(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user, self.status)

    class Meta:
        ordering = ['created_at']


class User_IP_B_List(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    login_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    black_list = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)