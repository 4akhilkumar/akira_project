from django.db import models
from django.contrib.auth.models import User

import uuid

from akira_apps.academic_registration.models import Course, SectionRooms
from akira_apps.staff.models import BLOOD_GROUP_CHOICES, GENDER_CHOICES

class Students(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    date_of_birth = models.DateField(default='1975-01-01')
    door_no = models.CharField(max_length=100, default="A-BCD, On Earth")
    zip_code = models.CharField(max_length=8, default="123456")
    city_name = models.CharField(max_length=50, default="Vijayawada")
    state_name = models.CharField(max_length=50, default="Andhra Pradesh")
    country_name = models.CharField(max_length=50, default="India")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='staffs/')
    current_medical_issue = models.TextField(max_length=50)
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["created_at"]

class course_registration_student(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    section = models.ForeignKey(SectionRooms, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('course','section')