from django.db import models
from django.contrib.auth.models import User
from akira_apps.academic_registration.models import Branch, SectionRooms, Semester
from akira_apps.student.models import Students
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

class Staffs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, unique=True, on_delete = models.CASCADE, help_text = 'Please Choose Faculty')
    gender = models.CharField(max_length=14, choices = GENDER_CHOICES, default=1, help_text = 'Please Choose Gender')
    father_name = models.CharField(max_length=100, default="Not Provided", help_text = 'Please Provide Your Father Name')
    father_occ = models.CharField(max_length=100, default="Not Provided", help_text = 'Please Provide Your Father Occupation')
    father_phone = models.CharField(max_length=10, default="9999999999", help_text = 'Please Provide Your Father Phone Number')
    mother_name = models.CharField(max_length=100, default="Not Provided", help_text = 'Please Provide Your Mother Name')
    mother_tounge = models.CharField(max_length=50, choices = MOTHER_TOUNGE_CHOICES, default=1, help_text = 'Please Choose Your Mother Tounge')
    dob = models.DateField(default='1975-01-01', help_text = 'Please Provide Your Date of Birth')
    blood_group = models.CharField(max_length=18, choices = BLOOD_GROUP_CHOICES, default=1, help_text = 'Please Choose Your Blood Group')
    phone = models.CharField(max_length=10, default="9999999999", help_text = 'Please Provide Your Phone Number')
    dno_sn = models.CharField(max_length=100, default="A-BCD, On Earth", help_text = 'Please Provide Your Door Number')
    zip_code = models.CharField(max_length=8, default="123456", help_text = 'Please Provide Your ZIP Code')
    city_name = models.CharField(max_length=50, default="Vijayawada", help_text = 'Please Provide Your Village, Town, City')
    state_name = models.CharField(max_length=50, default="Andhra Pradesh", help_text = 'Please Provide Your State Name')
    country_name = models.CharField(max_length=50, default="India", help_text = 'Please Provide Your Country')
    qualification = models.CharField(max_length=50, default="M.Tech", help_text = 'Please Provide Your Qualification')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Branch')
    designation = models.CharField(max_length=50, default="Assistant Professor", help_text = 'Please Provide Your Designation')
    profile_pic = models.ImageField(null=True, blank=True, default='avatar.webp', upload_to='staffs/', help_text = 'Please Provide Your Profile Photo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.user.first_name.title(), self.user.last_name.title())
    
    class Meta:
        ordering = ["user__username"]

class Course(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    course_code = models.CharField(max_length = 100, unique = True, help_text = 'Please Provide Course Code')
    course_name = models.CharField(max_length = 100, unique = True, help_text = 'Please Provide Course Name')
    course_desc = models.TextField(max_length = 500, unique = True, help_text = 'Upto 500 Charaters are allowed.')
    faculty = models.ForeignKey(Staffs, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Faculty')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Branch')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Semester')
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Student')
    room = models.ForeignKey(SectionRooms, on_delete=models.SET_NULL, blank=True, null=True, help_text = 'Please Choose Branch')

    def __str__(self):
        return '%s %s' % (self.course_code, self.course_name)

class CourseRegistration(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(Students, on_delete = models.CASCADE, help_text = 'Please Choose the Student')
    course = models.ForeignKey(Course, on_delete = models.CASCADE, help_text = 'Please Choose the Course')