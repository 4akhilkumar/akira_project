from django import template
from django.contrib.auth.models import User
from akira_apps.staff.models import (Staff)
from akira_apps.student.models import (Students)

register = template.Library()

@register.filter
def getUserProfile(value):
    user = User.objects.get(username=value)
    groupList = ', '.join(map(str, user.groups.all()))
    userImagePath = False
    if groupList is not None:
        if 'Student' in groupList:
            if Students.objects.filter(user__username = value).exists() is True:
                userObj = Students.objects.get(user__username = value)
                userImagePath = userObj.photo.url
        else:
            if Staff.objects.filter(user__username = value).exists() is True:
                userObj = Staff.objects.get(user__username = value)
                userImagePath = userObj.photo.url
        return userImagePath
    else:
        return userImagePath