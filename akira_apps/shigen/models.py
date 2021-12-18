from django.db import models
from django.contrib.auth.models import User

import uuid

class Resource(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='Resource/')
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='Resource/', null=True, blank=True, default="False")
    reference_info = models.CharField(max_length=100)
    hash_tags = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['created_at']