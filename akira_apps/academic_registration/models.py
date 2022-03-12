from django.contrib.auth.models import User
from django.db import models

import uuid

from akira_apps.specialization.models import (SpecializationsMC)

class SpecEnrollStudent(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    enrolledSpec = models.ForeignKey(SpecializationsMC, on_delete = models.SET_NULL, blank = True, null = True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.enrolledSpec)

    class Meta:
        unique_together = ['user','enrolledSpec']


# class academic_registration_staff(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True,)
#     branch = models.CharField(max_length = 50, unique = True, choices = BRANCH_CHOICES, default=1)

# class academic_registration_student(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     branch = models.CharField(max_length = 50, unique = True, choices = BRANCH_CHOICES, default=1)

# class specialization_registration_staff(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     specialization = models.ForeignKey(Specialization, on_delete = models.SET_NULL, blank = True, null = True)

# class specialization_registration_student(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     specialization = models.ForeignKey(Specialization, on_delete = models.SET_NULL, blank = True, null = True)

#     class Meta:
#         unique_together = ('student','specialization')

# class course_registration_staff(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
#     section = models.ForeignKey(SectionRooms, on_delete=models.SET_NULL, blank=True, null=True)

#     class Meta:
#         unique_together = ('course','section')