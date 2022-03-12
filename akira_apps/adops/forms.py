from django import forms
from .models import (JOB_TYPE_CHOICES, FIELD_VALUE_TYPE)

class OpeningsJobTypeForm(forms.Form):
    job_type = forms.ChoiceField(choices = JOB_TYPE_CHOICES)

class ExtraFieldValueTypeForm(forms.Form):
    field_value_type = forms.ChoiceField(choices = FIELD_VALUE_TYPE)