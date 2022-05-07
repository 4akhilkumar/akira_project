from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

import uuid

from akira_apps.academic_registration.models import (Branch)

JOB_TYPE_CHOICES = [
    ("", "Select Job Type"),
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Contract", "Contract"),
    ("Internship", "Internship"),
    ("Temporary", "Temporary"),
    ("Freelance", "Freelance"),
    ("Volunteer", "Volunteer"),
    ("Work From Home", "Work From Home"),
]

GENDER_CHOICES = [
    ("", "Select Gender"),
    ("Male", "Male"),
    ("Female", "Female"),
    ("Rather not say", "Rather not say"),
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

class UserProfile(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    name_prefix = models.CharField(max_length = 35, choices = Name_Prefix_Choices, default="", blank=True, null=True)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default="")
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default="")
    phone = models.CharField(max_length = 15)
    door_no = models.CharField(max_length=10)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    photo = models.ImageField(null=True, blank=True, upload_to='user_photos/', validators=[FileExtensionValidator(['webp','jpg', 'png', 'jpeg'])])

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["user__first_name"]

class Openings(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    job = models.CharField(max_length=100)
    overview = models.TextField(max_length=400)
    description = models.TextField(max_length=2000)
    experience = models.CharField(max_length=500)
    qualification = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    pay_scale = models.CharField(max_length=50)
    type = models.CharField(max_length=15, blank=True, null=True, choices = JOB_TYPE_CHOICES, default=1)
    contact_person = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    applied = models.ManyToManyField(User, related_name='applied_to', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.job)

    class Meta: 
        ordering = ['created_at']
        unique_together = ['job', 'location']

class TeachingStaffBranch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    teachingStaff = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.teachingStaff, self.branch)

    class Meta:
        unique_together = ['teachingStaff', 'branch']

class Programme(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    degree = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        unique_together = ['name', 'branch']

class ProgrammeExtraFields(models.Model):
    FIELD_TYPE = [
        ("", "Select Field type"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("number", "Number"),
    ]
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    field_name = models.CharField(max_length = 100)
    field_type = models.CharField(max_length = 100, choices = FIELD_TYPE, default="")
    field_value = models.TextField(max_length = 50000)

    def __str__(self):
        return '%s - %s' % (self.programme, self.field_name)

class Admission(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    batch_start_year = models.DateField()
    batch_end_year = models.DateField()
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.batch_start_year.strftime('%Y'), self.batch_end_year.strftime('%Y'))

    class Meta:
        unique_together = ['batch_start_year', 'batch_end_year', 'programme']

class AdmissionRegister(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    batch = models.ForeignKey(Admission, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.student, self.batch)
    
    class Meta:
        unique_together = ['user', 'batch']

class StuAdmAccountVerificationStatus(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bfpID = models.CharField(max_length = 100)
    ipaddress = models.GenericIPAddressField()
    verificationStatus = models.BooleanField(default = False)

    def __str__(self):
        return '%s - %s' % (self.user, self.verificationStatus)