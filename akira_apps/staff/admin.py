from django.contrib import admin
from akira_apps.staff.models import Staffs, Course_Sessions, CourseOutcome, CourseSession, CourseALMS, ALM

admin.site.register(Staffs)
admin.site.register(Course_Sessions)
admin.site.register(CourseOutcome)
admin.site.register(CourseSession)
admin.site.register(CourseALMS)
admin.site.register(ALM)