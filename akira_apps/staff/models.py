from django.db import models
from django.contrib.auth.models import User

import uuid

from akira_apps.academic.models import (Branch)

class Designation(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length = 500, null=True, blank=True)

    def __str__(self):
        return self.name

class UserDesignation(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.user, self.designation)
    
    class Meta:
        unique_together = ['user', 'designation', 'branch']

class Skills(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.name