from django import template
register = template.Library()
from akira_apps.course.models import (CourseTask)

@register.filter
def subComponent(value):
    getSubComponent = CourseTask.objects.filter(component__id=value)    
    return getSubComponent