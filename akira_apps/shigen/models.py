from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

import uuid
import os

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

@receiver(models.signals.post_delete, sender=Resource)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            try:
                os.remove(instance.video_file.path)
            except Exception:
                os.unlink(instance.video_file.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            try:
                os.remove(instance.thumbnail.path)
            except Exception:
                os.unlink(instance.thumbnail.path)