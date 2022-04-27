from django.db import models
from django.contrib.auth.models import User

import uuid

class URLShortenerMC(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ip_addr = models.GenericIPAddressField(blank=True, null=True)
    bfp_id = models.TextField(blank=True, null=True)
    long_url = models.TextField()
    long_url_path = models.CharField(max_length=20, unique=True)
    expire_date_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user, self.long_url_path)
    
    class Meta:
        ordering = ["user__username", "created_at"]

class ShortenURLStat(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    shortenURL = models.ForeignKey(URLShortenerMC, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    user_ip_address = models.GenericIPAddressField()
    os_details = models.CharField(max_length=40)
    browser_details = models.CharField(max_length=40)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user_ip_address, self.visited_at)

    class Meta:
        ordering = ["visited_at"]