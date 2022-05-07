from django import template
register = template.Library()
from akira_apps.course.models import (CourseCOTExtraFields)

@register.filter
def COTExtraFieldData(value):
    getCOTExtraFieldsData = CourseCOTExtraFields.objects.filter(course__id=value)
    return getCOTExtraFieldsData