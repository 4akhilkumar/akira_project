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
    score = models.IntegerField(blank=True, null=True)
    attempt = models.CharField(max_length=100)
    user_confirm = models.CharField(max_length=100, blank=True, null=True, default='Pending')
    reason = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s | %s' % (self.user, self.user_ip_address, self.created_at.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        ordering = ['created_at']

class User_IP_B_List(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    login_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    black_list = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.black_list)

    class Meta:
        ordering = ['created_at']

class User_IP_S_List(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    login_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    suspicious_list = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s | %s' % (self.suspicious_list, self.created_at.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        ordering = ['created_at']

class User_BackUp_Codes(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, unique=True, on_delete=models.SET_NULL, blank=True, null=True)
    backup_codes = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']

class User_BackUp_Codes_Login_Attempts(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    attempt = models.IntegerField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']