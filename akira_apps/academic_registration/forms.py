from django import forms
from django.db import models

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