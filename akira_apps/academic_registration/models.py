from enum import unique
from django.contrib.auth.models import User
from django.db import models

import uuid

from ckeditor_uploader.fields import RichTextUploadingField

class Semester(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    mode = models.CharField(max_length = 4, choices = MODE, default = 1)
    start_year = models.DateField()
    end_year = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' % (self.mode, self.start_year.year)

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

# class academic_registration_staff(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True,)
#     branch = models.CharField(max_length = 50, unique = True, choices = BRANCH_CHOICES, default=1)

# class academic_registration_student(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     branch = models.CharField(max_length = 50, unique = True, choices = BRANCH_CHOICES, default=1)

# class Specialization(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     specialization_name = models.CharField(max_length = 50, unique = True)
#     specialization_short_info = models.TextField(max_length = 100, default="Start your path to a career in project management. No degree or experience is required.")
#     specialization_wywl = models.TextField(max_length = 500, default="WHAT YOU WILL LEARN")
#     specialization_sywg = models.TextField(max_length = 500, default="SKILLS YOU WILL GAIN")
#     specialization_desc = RichTextUploadingField()
#     specialization_faculty = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     branch = models.CharField(max_length = 50, unique = True, choices = BRANCH_CHOICES, default=1)
#     capacity = models.IntegerField(default=0)

#     def __str__(self):
#         return '%s' % (self.specialization_name)

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

class Course(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course_code = models.CharField(max_length = 100, unique = True)
    course_name = models.CharField(max_length = 100, unique = True)
    course_short_info = models.TextField(max_length = 500, default="Start your path to a career in project management. No degree or experience is required.")
    course_wywl = models.TextField(max_length = 500, default="WHAT YOU WILL LEARN")
    course_sywg = models.TextField(max_length = 500, default="SKILLS YOU WILL GAIN")
    course_desc = RichTextUploadingField()
    course_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.CharField(max_length = 50, choices = BRANCH_CHOICES, default=1)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.course_code, self.course_name)

# class course_registration_staff(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
#     section = models.ForeignKey(SectionRooms, on_delete=models.SET_NULL, blank=True, null=True)

#     class Meta:
#         unique_together = ('course','section')


# updateUser = User.objects.get(username = '4akhi')
# updateUser.first_name = 'Sai Akhil Kumar Reddy'
# updateUser.last_name = 'N'
# updateUser.save()
# listUser = User.objects.all()
# print(listUser)