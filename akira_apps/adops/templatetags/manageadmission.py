from django import template
from django.contrib.auth.models import User, Group
register = template.Library()


@register.filter
def onlyYear(value):
    try:
        only_year = value.strftime('%Y')
        return only_year
    except Exception:
        return value

@register.filter
def admissionStatus(value):
    getStudent = User.objects.get(username = value)
    if getStudent.groups.filter(name = 'Admission Student').exists() is True:
        studentGroup, created = Group.objects.get_or_create(name='Student')
        studentGroup.user_set.add(getStudent)
        admStudentGroup, created = Group.objects.get_or_create(name='Admission Student')
        admStudentGroup.user_set.remove(getStudent)
        return True
    elif getStudent.groups.filter(name = 'Student').exists() is True:
        return False
    else:
        return None