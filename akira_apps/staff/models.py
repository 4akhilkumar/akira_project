from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
import uuid

from akira_apps.academic_registration.models import Course

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

class Staffs(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE)
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1)
    date_of_birth = models.DateField(default='1975-01-01')
    door_no = models.CharField(max_length=100, default="A-BCD, On Earth")
    zip_code = models.CharField(max_length=8, default="123456")
    city_name = models.CharField(max_length=50, default="Vijayawada")
    state_name = models.CharField(max_length=50, default="Andhra Pradesh")
    country_name = models.CharField(max_length=50, default="India")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='staffs/')
    current_medical_issue = models.TextField(max_length=50)
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["created_at"]

class Course_Sessions(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='Course_Sessions/%s/' % str(name))
    description = RichTextUploadingField()
    video_file = models.FileField(upload_to='Course_Sessions/', null=True, blank=True, default="False")
    reference_info = RichTextUploadingField()
    hash_tags = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class CourseOutcome(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)

class CourseSession(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    course_outcome = models.ForeignKey(CourseOutcome, on_delete=models.SET_NULL, blank=True, null=True)

class CourseALMS(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    course_outcome = models.ForeignKey(CourseOutcome, on_delete=models.SET_NULL, blank=True, null=True)
    course_session = models.ForeignKey(CourseSession, on_delete=models.SET_NULL, blank=True, null=True)

class ALMSubmission(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    course_outcome = models.ForeignKey(CourseOutcome, on_delete=models.SET_NULL, blank=True, null=True)
    course_session = models.ForeignKey(CourseSession, on_delete=models.SET_NULL, blank=True, null=True)
    # course_alm = models.ForeignKey(ALM, on_delete=models.SET_NULL, blank=True, null=True)
    student = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    answer = models.FileField(upload_to='%s/ALM_Submissions/' % str(course))

class ALM(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    course_outcome = models.ForeignKey(CourseOutcome, on_delete=models.SET_NULL, blank=True, null=True)
    course_session = models.ForeignKey(CourseSession, on_delete=models.SET_NULL, blank=True, null=True)
    staff = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True)
    course_session = models.ForeignKey(ALMSubmission, on_delete=models.SET_NULL, blank=True, null=True)
    question = RichTextUploadingField()