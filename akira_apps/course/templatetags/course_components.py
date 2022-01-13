from django import template
register = template.Library()
from akira_apps.course.models import (CourseComponent, CourseMC, CourseFiles, CourseSubComponent, CourseTask, TaskAnswer)

@register.filter
def subComponent(value):
    getSubComponent = CourseTask.objects.filter(component__id=value)    
    return getSubComponent