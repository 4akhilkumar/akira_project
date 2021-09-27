from django.db import models
from django.contrib.auth.models import User
import uuid

class UserLoginDetails(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    user_ip_address = models.CharField(max_length=100)
    os_details = models.CharField(max_length=100)
    browser_details = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user, self.user_ip_address)

    class Meta:
        ordering = ['-created_at']