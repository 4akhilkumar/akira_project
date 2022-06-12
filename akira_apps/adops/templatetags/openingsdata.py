from tkinter.filedialog import Open
from django import template
register = template.Library()

from django.db.models import IntegerField
from django.db.models.functions import Cast

import math

from akira_apps.adops.models import (Openings)
from akira_apps.academic.models import (Academy)

@register.filter
def getJobTypeCount(value):
    return Openings.objects.filter(type=value).count()

@register.filter
def getSalaryDisclosed(value):
    return Openings.objects.filter(pay_scale = "Not Disclosed").count() or " "

@register.filter
def getMinMaxJobSalaryRange(value):
    minMaxSalaries = set()
    for job in Openings.objects.all():
        if job.pay_scale.isnumeric():
            miniSalary = int(math.pow(10, len(job.pay_scale) - 1) + 1)
            maxiSalary = int(math.pow(10, len(job.pay_scale)))
            rangeSal = "&#8377;" + str(miniSalary) + " - " + "&#8377;" +  str(maxiSalary)
            minMaxSalaries.add(rangeSal)
    return minMaxSalaries

@register.filter
def salaryRangeCount(value):
    val = str(value).replace("&#8377;", "").split(" - ")
    minSalRange = val[0]
    maxSalRange = val[1]
    try:
        minmaxSalRange = Openings.objects.annotate(
            pay_scale_as_int=Cast('pay_scale', IntegerField())
            ).filter(
                pay_scale_as_int__gte = minSalRange, pay_scale_as_int__lte = maxSalRange
                ).count()
        return minmaxSalRange
    except Exception:
        return " "

@register.filter
def instituteName(value):
    acaObj = Academy.objects.all().first()
    return acaObj.name