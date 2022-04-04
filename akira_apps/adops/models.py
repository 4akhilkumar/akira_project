from django.contrib.auth.models import User
from django.db import models

import uuid

JOB_TYPE_CHOICES = [
    ("", "Select Job Type"),
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Contract", "Contract"),
    ("Internship", "Internship"),
    ("Temporary", "Temporary"),
    ("Freelance", "Freelance"),
    ("Volunteer", "Volunteer"),
    ("Work From Home", "Work From Home"),
]

class Openings(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    job = models.CharField(max_length=100)
    overview = models.TextField(max_length=400)
    description = models.TextField(max_length=2000)
    experience = models.CharField(max_length=20)
    qualification = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    pay_scale = models.CharField(max_length=50)
    type = models.CharField(max_length=15, blank=True, null=True, choices = JOB_TYPE_CHOICES, default=1)
    contact_person = models.ForeignKey(User, on_delete=models.CASCADE)
    applied = models.ManyToManyField(User, related_name='applied_to', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.job)

    class Meta: 
        ordering = ['created_at']
        unique_together = ['job', 'location']

FIELD_VALUE_TYPE = [
    ("", "Select Field Value Type"),
    ("text", "text"),
    ("number", "number"),
    ("textarea", "textarea"),
]

class ExtraFieldOpenings(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.TextField(max_length=500)
    value = models.TextField(max_length=500)
    value_type = models.CharField(max_length=10,  choices = FIELD_VALUE_TYPE, default=1)
    mappingto = models.ForeignKey(Openings, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)