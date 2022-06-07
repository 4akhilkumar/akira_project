from django import template
from django.contrib.auth.models import User

register = template.Library()

from akira_apps.academic_registration.models import (SetSemesterRegistration, Semester)
from akira_apps.course.models import (CourseMC)
from akira_apps.staff.models import (UserDesignation)

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

@register.filter
def getSemesterByUserDesignationBranch(value):
    try:
        if User.objects.filter(username = value).exists() is True:
            user = User.objects.get(username = value)
            groupName = user.groups.all()[0].name
            if groupName == "Administrator":
                semesters = Semester.objects.all().order_by('-start_year')
            else:
                getDesignationBranch = UserDesignation.objects.get(user__username = value)
                semesters = Semester.objects.filter(branch__name = getDesignationBranch.branch.name)
            return semesters
    except Exception:
        return False