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
        Seventh = 'Seventh'
        Eighth = 'Eighth'
        Ninth = 'Ninth'
        Tenth = 'Tenth'
        Eleventh = 'Eleventh'
    floor = forms.ChoiceField(choices = Floor.choices)
    fields = ['floor']

class RoomTypeForm(forms.Form):
    TYPE = [
        ('Class Room','Class Room'),
        ('Staff Room','Staff Room'),
        ('Waiting Hall','Waiting Hall'),
        ('Lab','Lab'),
        ('Meeting Hall','Meeting Hall'),
    ]
    roomTypeForm = forms.ChoiceField(choices = TYPE)