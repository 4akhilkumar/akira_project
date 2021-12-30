from django.contrib.auth.models import User
from django.db import models

import uuid

class SpecializationsMC(models.Model):
    BRANCH_CHOICES = [
        ("","Branch Name"),
        ("Computer Science and Engineering","Computer Science and Engineering"),
        ("Aerospace/aeronautical Engineering","Aerospace/aeronautical Engineering"),
        ("Chemical Engineering","Chemical Engineering"),
        ("Civil Engineering","Civil Engineering"),
        ("Electronics and Communications Engineering","Electronics and Communications Engineering"),
        ("Electrical and Electronics Engineering","Electrical and Electronics Engineering"),
        ("Petroleum Engineering","Petroleum Engineering"),
        ("Bio Technology","Bio Technology"),
        ("Mechanical Engineering","Mechanical Engineering"),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    specialization_name = models.CharField(max_length = 50, unique = True)
    specialization_short_info = models.TextField(max_length = 100, default="Start your path to a career in project management. No degree or experience is required.")
    specialization_wywl = models.TextField(max_length = 500, default="WHAT YOU WILL LEARN")
    specialization_sywg = models.TextField(max_length = 500, default="SKILLS YOU WILL GAIN")
    specialization_desc = models.TextField(max_length = 500, default="Description of the Specialization")
    specialization_faculty = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.CharField(max_length = 50, choices = BRANCH_CHOICES, default=1)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.specialization_name)

class SpecializationFiles(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    specialization = models.ForeignKey(SpecializationsMC, on_delete=models.CASCADE)
    specialization_files = models.FileField(upload_to='Specialization_Files/', blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.specialization, self.specialization_files)