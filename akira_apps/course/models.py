from django.contrib.auth.models import User
from django.db import models

import uuid

from akira_apps.academic.models import (Semester)

class Course(models.Model):
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
    course_code = models.CharField(max_length = 100, unique = True)
    course_name = models.CharField(max_length = 100, unique = True)
    course_short_info = models.TextField(max_length = 500, default="Start your path to a career in project management. No degree or experience is required.")
    course_wywl = models.TextField(max_length = 500, default="WHAT YOU WILL LEARN")
    course_sywg = models.TextField(max_length = 500, default="SKILLS YOU WILL GAIN")
    course_desc = models.TextField(max_length = 500, default="Description of the Course")
    course_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.CharField(max_length = 50, choices = BRANCH_CHOICES, default=1)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course_code, self.course_name)

class CourseFiles(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_files = models.FileField(upload_to='Course Files/', blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.course_files)