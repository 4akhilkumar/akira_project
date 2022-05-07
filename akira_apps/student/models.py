from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import uuid
import datetime as pydt

def atLeastAgeofMajority(value):
    inputDate = str(value)
    inputDate = pydt.datetime.strptime(inputDate, '%Y-%m-%d')
    today = pydt.datetime.today()
    diff = today - inputDate
    if not ((diff.days//365) >= 18):
        raise ValidationError("You are not 18 years old.")
    inputDate = str(value)
    inputDate = pydt.datetime.strptime(inputDate, '%Y-%m-%d')
    current_year = pydt.datetime.today().year
    max_year = int(current_year) - 18
    # min_year = int(max_year) - 3
    year = inputDate.year
    if year <= max_year:
        today = pydt.datetime.today()
        diff = today - inputDate
        if not ((diff.days//365) >= 18):
            raise ValidationError("You are not 18 years old.")
    else:
        raise ValidationError("Invalid DOB")