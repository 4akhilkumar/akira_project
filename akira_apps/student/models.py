from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


import uuid
import datetime as pydt

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

def atLeastAgeofMajority(value):
    inputDate = str(value)
    inputDate = pydt.datetime.strptime(inputDate, '%Y-%m-%d')
    today = pydt.datetime.today()
    diff = today - inputDate
    if not ((diff.days//365) >= 18):
        raise ValidationError("You are not 18 years old.")
    inputDate = str(value)
    inputDate = pydt.datetime.strptime(inputDate, '%Y-%m-%d')
    current_year = pydt.datetime.today().year
    max_year = int(current_year) - 18
    # min_year = int(max_year) - 3
    year = inputDate.year
    if year <= max_year:
        today = pydt.datetime.today()
        diff = today - inputDate
        if not ((diff.days//365) >= 18):
            raise ValidationError("You are not 18 years old.")
    else:
        raise ValidationError("Invalid DOB")

class Students(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    date_of_birth = models.DateField(validators = [atLeastAgeofMajority])
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    door_no = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo = models.ImageField(null=True, blank=True, upload_to='student_photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())

# class course_registration_student(models.Model):
#     id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
#     student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
#     course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
#     section = models.ForeignKey(SectionRooms, on_delete=models.SET_NULL, blank=True, null=True)

#     class Meta:
#         unique_together = ('course','section')