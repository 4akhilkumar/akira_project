from django.contrib.auth.models import User
from django import template
register = template.Library()

from akira_apps.staff.models import (Staff)

@register.filter
def applicantPhoto(value):
    userObj = User.objects.get(id=value)
    staff = Staff.objects.get(user=userObj)
    return staff.photo.url

@register.filter
def about(value):
    userObj = User.objects.get(id=value)
    staff = Staff.objects.get(user=userObj)
    if staff.about:
        return staff.about
    else:
        loremText = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Animi, dolores aut. Nisi nulla facere dicta itaque sed nemo doloribus? Aut!"
        return loremText

@register.filter
def skills(value):
    userObj = User.objects.get(id=value)
    staff = Staff.objects.get(user=userObj)
    skills = staff.skills.all()
    skills_list = []
    for skill in skills:
        skills_list.append(skill.name)
    if skills_list:
        return skills_list
    else:
        return False

@register.filter
def isResume(value):
    userObj = User.objects.get(id=value)
    staff = Staff.objects.get(user=userObj)
    if staff.resume:
        return True
    else:
        return False