from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

import uuid

from akira_apps.academic.models import (Branch)

GENDER_CHOICES = [
    ("", "Select Gender"),
    ("Male", "Male"),
    ("Female", "Female"),
]

BLOOD_GROUP_CHOICES = [
    ("","Blood Group"),
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("O+","O+"),
    ("O-","O-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
]

MOTHER_TOUNGE_CHOICES = [
    ("","Mother Tounge"),
    ("Hindi","Hindi"),
    ("English","English"),
    ("Bengali","Bengali"),
    ("Marathi","Marathi"),
    ("Telugu","Telugu"),
    ("Tamil","Tamil"),
    ("Gujarati","Gujarati"),
    ("Urdu","Urdu"),
    ("Kannada","Kannada"),
    ("Odia","Odia"),
    ("Malayalam","Malayalam"),
    ("Punjabi","Punjabi"),
]

Name_Prefix_Choices = [
    ("","Select Name Prefix"),
    ("Dean","University Dean"),
    ("Dr","Doctor (Medical or Educator)"),
    ("Hon","Honorable"),
    ("Mr","Mister"),
    ("Mrs","Married Woman"),
    ("Ms","Single/Unmarried Women"),
    ("Prof","Professor"),
]

class Staff(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    name_prefix = models.CharField(max_length = 35, choices = Name_Prefix_Choices, default=1)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    phone = models.CharField(max_length = 15)
    door_no = models.CharField(max_length=10)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo = models.ImageField(null=True, blank=True, upload_to='staff_photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    branch = models.ForeignKey(Branch, on_delete = models.DO_NOTHING, blank = True, null = True)
    about = models.TextField(max_length=500, null=True, blank=True)
    skills = models.ManyToManyField('Skills', blank = True)
    resume = models.FileField(upload_to ='staff_resumes/', validators=[FileExtensionValidator(['pdf'])], blank = True, null = True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["user__first_name"]

class Skills(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.name

# class UserExtraFields(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     staffMC = models.ForeignKey(Staff, on_delete = models.CASCADE)
#     field_name = models.CharField(max_length = 100)
#     field_value = models.TextField(max_length=500)

#     def __str__(self):
#         return '%s' % (self.field_name)