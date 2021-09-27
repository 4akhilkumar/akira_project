from django.contrib import admin
from .models import Staffs, Course,CourseRegistration

admin.site.register(Staffs)
admin.site.register(Course)
admin.site.register(CourseRegistration)