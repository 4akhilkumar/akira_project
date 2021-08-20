from django.db import models
from django.contrib.auth.models import User
from akira_apps.academic_registration.models import Branch, Semester

import uuid

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

class Students(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE, help_text = 'Please Choose the Student')
    gender = models.CharField(max_length = 14, choices = GENDER_CHOICES, default = 1, help_text = 'Please Choose Gender')
    father_name = models.CharField(max_length = 100, default = "Not Provided", help_text = 'Please Provide Your Father Name')
    father_occ = models.CharField(max_length = 100, default = "Not Provided", help_text = 'Please Provide Your Father Occupation', verbose_name='Father Occupation')
    father_phone = models.CharField(max_length = 10, default = "9999999999", help_text = 'Please Provide Your Father Phone Number')
    mother_name = models.CharField(max_length = 100, default = "Not Provided", help_text = 'Please Provide Your Mother Name')
    mother_tounge = models.CharField(max_length = 50, choices = MOTHER_TOUNGE_CHOICES, default = 1, help_text = 'Please Choose Your Mother Tounge')
    dob = models.DateField(default = '1998-01-01', help_text = 'Please Provide Your Date of Birth', verbose_name='Date of Birth')
    blood_group = models.CharField(max_length = 18, choices = BLOOD_GROUP_CHOICES, default = 1, help_text = 'Please Choose Your Blood Group')
    phone = models.CharField(max_length = 10, default = "9999999999", help_text = 'Please Provide Your Phone Number')
    dno_sn = models.CharField(max_length = 100, default = "A-BCD, On Earth", help_text = 'Please Provide Your Door Number', verbose_name='Door Number')
    zip_code = models.CharField(max_length=8, default = "123456", help_text = 'Please Provide Your ZIP Code')
    city_name = models.CharField(max_length = 50, default = "Vijayawada", help_text = 'Please Provide Your Village, Town, City')
    state_name = models.CharField(max_length = 50, default = "Andhra Pradesh", help_text = 'Please Provide Your State Name')
    country_name = models.CharField(max_length = 50, default = "India", help_text = 'Please Provide Your Country')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Branch')
    profile_pic = models.ImageField(null = True, blank = True, default = 'avatar.webp', upload_to='students/', help_text = 'Please Provide Your Profile Photo')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["user__username"]

class SemesterStatus(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(Students, on_delete = models.CASCADE, help_text = 'Please Choose the Student')
    semester = models.ForeignKey(Semester, on_delete = models.CASCADE, help_text = 'Please Choose the Semester')
    status = models.BooleanField()

    def __str__(self):
        return '%s %s' % (self.user, self.status)