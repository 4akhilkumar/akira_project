from django.db import models
from django.contrib.auth.models import User

import uuid

User._meta.get_field('email')._unique = True

class UserLoginDetails(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ip_address = models.GenericIPAddressField()
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
    login_user = models.ForeignKey(User, on_delete=models.CASCADE)
    black_list = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.black_list)

    class Meta:
        ordering = ['created_at']

class User_IP_S_List(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    login_user = models.ForeignKey(User, on_delete=models.CASCADE)
    suspicious_list = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s | %s' % (self.suspicious_list, self.created_at.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        ordering = ['created_at']

class User_BackUp_Codes(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    backup_codes = models.TextField(max_length=100)
    download = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']

class User_BackUp_Codes_Login_Attempts(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userIPAddr = models.GenericIPAddressField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']

class SwitchDevice(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userIPAddr = models.GenericIPAddressField()
    userBrowser = models.CharField(max_length=100)
    userOS = models.CharField(max_length=100)
    userConfirm = models.CharField(max_length=100, blank=True, null=True, default='Pending')
    reason = models.CharField(max_length=100, blank=True, null=True)
    currentPage = models.TextField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=100, default="Switch Device Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']

class UserPageVisits(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userIPAddr = models.GenericIPAddressField()
    currentPage = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta:
        ordering = ['created_at']