from django.contrib.auth.models import User
from django.db import models

import uuid

class TwoFactorAuth(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    twofa = models.BooleanField(default = False)
    changed_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.user)

    class Meta: 
        ordering = ['changed_on']