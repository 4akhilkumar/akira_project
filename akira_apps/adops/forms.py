from django import forms
from .models import (JOB_TYPE_CHOICES)

class OpeningsJobTypeForm(forms.Form):
    job_type = forms.ChoiceField(choices = JOB_TYPE_CHOICES)