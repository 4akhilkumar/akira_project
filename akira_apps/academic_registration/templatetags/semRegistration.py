from django import template
register = template.Library()

from akira_apps.academic_registration.models import (SetSemesterRegistration, Semester)
from akira_apps.course.models import (CourseMC)

@register.filter
def checkTeachingStaffSemRegStatus(value):
    try:
        semesterObj = Semester.objects.get(id=value)
        getSemRegStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
        return getSemRegStatus.teachingstaff
    except Exception:
        return False

@register.filter
def checkStudentSemRegStatus(value):
    try:
        semesterObj = Semester.objects.get(id=value)
        getSemRegStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
        return getSemRegStatus.students
    except Exception:
        return False

@register.filter
def checkTeachingStaffSemRegCourse(value):
    try:
        getCourseSem = CourseMC.objects.get(id=value)
        semesterObj = Semester.objects.get(id=getCourseSem.semester.id)
        getSemRegStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
        return getSemRegStatus.teachingstaff
    except Exception:
        return False

@register.filter
def checkStudentSemRegCourse(value):
    try:
        getCourseSem = CourseMC.objects.get(id=value)
        semesterObj = Semester.objects.get(id=getCourseSem.semester.id)
        getSemRegStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
        return getSemRegStatus.students
    except Exception:
        return False