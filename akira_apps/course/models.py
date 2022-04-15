from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

import uuid
import os

from akira_apps.academic.models import (Semester, Branch)
from akira_apps.specialization.models import (SpecializationsMC)

class CourseMC(models.Model):
    COURSE_TYPE = [
        ("", "Course Type"),
        ("Professional Elective", "Professional Elective"),
        ("Foreign Language Elective", "Foreign Language Elective"),
        ("Open Elective", "Open Elective"),
        ("Science Elective", "Science Elective"),
        ("NDY", "NDY"),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    code = models.CharField(max_length = 100, unique = True)
    name = models.CharField(max_length = 100, unique = True)
    desc = models.TextField(max_length = 500)
    course_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)
    specialization = models.ForeignKey(SpecializationsMC, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length = 50, choices = COURSE_TYPE, default=1)
    pre_requisite = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.code, self.name)

class CourseExtraFields(models.Model):
    FIELD_TYPE = [
        ("", "Select Field type"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("number", "Number"),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    field_name = models.CharField(max_length = 100)
    field_type = models.CharField(max_length = 100, choices = FIELD_TYPE, default="")
    field_value = models.TextField(max_length = 50000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.field_name)

class CourseOfferingType(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    name = models.CharField(max_length = 40)
    l = models.IntegerField(default=0)
    t = models.IntegerField(default=0)
    p = models.IntegerField(default=0)
    s = models.IntegerField(default=0)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

class CourseCOTExtraFields(models.Model):
    FIELD_TYPE = [
        ("", "Select Field type"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("number", "Number"),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseOfferingType, on_delete=models.CASCADE)
    field_name = models.CharField(max_length = 100)
    field_type = models.CharField(max_length = 100, choices = FIELD_TYPE, default="")
    field_value = models.TextField(max_length = 50000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.field_name)

class CourseFiles(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    course_files = models.FileField(upload_to='Course_Files/', blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.course_files)

@receiver(models.signals.post_delete, sender=CourseFiles)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.course_files:
        if os.path.isfile(instance.course_files.path):
            try:
                os.remove(instance.course_files.path)
            except Exception:
                os.unlink(instance.course_files.path)

class CourseComponent(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 500, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

class CourseSubComponent(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    component = models.ForeignKey(CourseComponent, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 500, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

class CourseTask(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    sub_component = models.ForeignKey(CourseSubComponent, on_delete=models.CASCADE)
    question = models.TextField(max_length = 500)
    answer = models.ForeignKey('TaskAnswer', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.question)

class TaskAnswer(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(CourseTask, on_delete=models.CASCADE)
    answer = models.FileField(upload_to='TaskAnswerFiles/')

    def __str__(self):
        return '%s - %s' % (self.user, self.answer) 