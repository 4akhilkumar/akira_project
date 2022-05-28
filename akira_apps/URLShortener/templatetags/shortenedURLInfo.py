from django import template

from akira_apps.URLShortener.models import (URLShortenerMC, ShortenURLStat)

import datetime as pydt

register = template.Library()

@register.filter
def totalClicks(value):
    usmcObj = URLShortenerMC.objects.get(id = value)
    return ShortenURLStat.objects.filter(shortenURL=usmcObj).count()

@register.filter
def abouttoexpire(value):
    if URLShortenerMC.objects.filter(id = value, expire_date_time__gt = pydt.datetime.now()).exists():
        return True
    else:
        return False