from django.contrib.auth.models import User
from django.db import models

import uuid

from akira_apps.course.models import (CourseMC)

class Branch(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique = True)
    description = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['name']

class Semester(models.Model):
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    mode = models.CharField(max_length = 4, choices = MODE, default = 1)
    start_year = models.DateField()
    end_year = models.DateField()
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s - %s' % (self.mode, self.start_year.year, self.branch.name)

    class Meta:
        ordering = ['-start_year']

class DesignCoursesSemester(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    semester = models.OneToOneField(Semester, on_delete=models.CASCADE)
    course = models.ManyToManyField(CourseMC)

class SetSemesterRegistration(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    semester = models.OneToOneField(Semester, on_delete = models.CASCADE)
    teachingstaff = models.BooleanField(default = False)
    students = models.BooleanField(default = False)

    def __str__(self):
        return '%s - %s - %s ' % (self.semester, self.teachingstaff, self.students)

class TeachingStaffSemRegistration(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE)
    teachingStaff = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return '%s - %s ' % (self.semester, self.staff)

    class Meta:
        unique_together = ['semester','teachingStaff']

class StudentSemRegistration(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE)
    student = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return '%s - %s ' % (self.semester, self.student)

    class Meta:
        unique_together = ['semester','student']