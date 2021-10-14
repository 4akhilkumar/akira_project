from django.contrib import admin
from akira_apps.academic_registration.models import Block, SectionRooms, Semester, academic_registration_staff, academic_registration_student, Specialization, specialization_registration_staff, specialization_registration_student, Course, course_registration_staff

admin.site.register(Block)
admin.site.register(SectionRooms)
admin.site.register(Semester)
admin.site.register(academic_registration_staff)
admin.site.register(academic_registration_student)
admin.site.register(Specialization)
admin.site.register(specialization_registration_staff)
admin.site.register(specialization_registration_student)
admin.site.register(Course)
admin.site.register(course_registration_staff)