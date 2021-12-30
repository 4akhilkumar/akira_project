from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

import uuid
import os

from akira_apps.academic.models import (Semester)
from akira_apps.specialization.models import (SpecializationsMC)

class CourseMC(models.Model):
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
    specialization = models.ForeignKey(SpecializationsMC, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course_code, self.course_name)

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
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    component = models.ForeignKey(CourseComponent, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 500, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

class CourseTask(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    component = models.ForeignKey(CourseComponent, on_delete=models.CASCADE)
    sub_component = models.ForeignKey(CourseSubComponent, on_delete=models.CASCADE)
    question = models.TextField(max_length = 500)
    answer = models.ForeignKey('TaskAnswer', on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.question)

class TaskAnswer(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseMC, on_delete=models.CASCADE)
    component = models.ForeignKey(CourseComponent, on_delete=models.CASCADE)
    sub_component = models.ForeignKey(CourseSubComponent, on_delete=models.CASCADE)
    task = models.ForeignKey(CourseTask, on_delete=models.CASCADE)
    answer = models.FileField(upload_to='TaskAnswerFiles/')

    def __str__(self):
        return '%s - %s' % (self.user, self.answer)