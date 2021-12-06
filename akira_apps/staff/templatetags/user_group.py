from django.contrib.auth.models import User
from django import template
register = template.Library()

@register.filter
def user_group(value):
    user = User.objects.get(username=value)
    groupList = ', '.join(map(str, user.groups.all()))
    return groupList