from django import template
from django.contrib.auth.models import User
from akira_apps.adops.models import (UserProfile)

register = template.Library()

@register.filter
def getUserProfile(value):
    try:
        user = User.objects.get(username=value)
    except User.DoesNotExist:
        return False
    groupList = ', '.join(map(str, user.groups.all()))
    userImagePath = False
    if groupList is not None:
        if UserProfile.objects.filter(user__username = value).exists() is True:
            userObj = UserProfile.objects.get(user__username = value)
            if userObj.photo:
                userImagePath = userObj.photo.url
            else:
                return False
        return userImagePath
    else:
        return userImagePath