from django import forms
from django.db import models

from akira_apps.academic_registration.models import BRANCH_CHOICES, Semester, Course

class SemesterForm(forms.Form):
    SEM_MODE = (
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    )
    model = Semester
    mode = forms.ChoiceField(choices = SEM_MODE)
    fields = ['mode']

class BranchForm(forms.Form):
    branch = forms.ChoiceField(choices = BRANCH_CHOICES)
    fields = ['branch']

class SectionRoomForm(forms.Form):
    class Floor(models.TextChoices):
        Ground = 'Ground'
        First = 'First'
        Second = 'Second'
        Third = 'Third'
        Fourth = 'Fourth'
        Fifth = 'Fifth'
        Sixth = 'Sixth'
    floor = forms.ChoiceField(choices = Floor.choices)
    fields = ['floor']