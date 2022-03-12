from django.db import models
from django.contrib.auth.models import User

import uuid

class MailLog(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.TextField(max_length = 1024)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '%s - %s' % (self.user, self.subject)
    
    class Meta:
        ordering = ["created_at"]