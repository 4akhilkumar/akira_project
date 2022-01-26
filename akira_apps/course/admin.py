from django.contrib import admin
from .models import (CourseMC, CourseFiles,
                    CourseComponent, CourseSubComponent,
                    TaskAnswer, CourseTask, CourseOfferingType)

admin.site.register(CourseMC)
admin.site.register(CourseFiles)
admin.site.register(CourseComponent)
admin.site.register(CourseSubComponent)
admin.site.register(TaskAnswer)
admin.site.register(CourseTask)
admin.site.register(CourseOfferingType)