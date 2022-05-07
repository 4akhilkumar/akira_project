from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

import uuid

class Designation(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length = 500, null=True, blank=True)

    def __str__(self):
        return self.name

class Skills(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.name