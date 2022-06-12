from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

import uuid

from akira_apps.academic_registration.models import (Branch, Semester)

class UserProfile(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    name_prefix = models.CharField(max_length = 35)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=8)
    gender = models.CharField(max_length=14)
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
    overview = models.TextField(max_length=1000)
    description = models.TextField(max_length=2000)
    experience = models.CharField(max_length=2000)
    qualification = models.CharField(max_length=2000)
    location = models.CharField(max_length=100)
    pay_scale = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    contact_person = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    applied = models.ManyToManyField(User, related_name='applied_to', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.job)

    class Meta: 
        ordering = ['created_at']
        unique_together = ['job', 'location']

class StaffBranch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    staff = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.staff, self.branch)

    class Meta:
        unique_together = ['staff', 'branch']

class Batch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    start_year = models.DateField()
    end_year = models.DateField()

    class Meta:
        ordering = ['start_year']

class BatchProgramSemester(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, blank=True, null=True)
    program = models.ForeignKey('Programme', on_delete=models.SET_NULL, blank=True, null=True)
    semester = models.ManyToManyField(Semester)

class Programme(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    degree = models.CharField(max_length=100) # B.Tech, B.Sc, M.Tech, M.Sc, M.Des, M.Des. etc.
    name = models.CharField(max_length=100, unique=True)
    duration = models.DurationField()
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        unique_together = ['name', 'branch']

class ProgrammeExtraFields(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    field_name = models.CharField(max_length = 100)
    field_type = models.CharField(max_length = 100)
    field_value = models.TextField(max_length = 50000)

    def __str__(self):
        return '%s - %s' % (self.programme, self.field_name)

class Admission(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, blank=True, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.batch_start_year.strftime('%Y'), self.batch_end_year.strftime('%Y'))

class AdmissionRegister(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    batch = models.ForeignKey(Admission, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.student, self.batch)
    
    class Meta:
        unique_together = ['student', 'batch']

class UserAccountVerificationStatus(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bfpID = models.CharField(max_length = 100, blank = True, null = True)
    ipaddress = models.GenericIPAddressField()
    verificationStatus = models.BooleanField(default = False)

    def __str__(self):
        return '%s - %s' % (self.user, self.verificationStatus)