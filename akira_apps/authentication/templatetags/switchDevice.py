from django import template
from django.contrib.sessions.models import Session

from akira_apps.authentication.models import SwitchDevice

register = template.Library()

@register.filter
def checkSessionKey(value):
    currentSDReq = SwitchDevice.objects.get(id=value)
    try:
        Session.objects.get(session_key=currentSDReq.sessionKey)
        return True
    except Exception:
        return False