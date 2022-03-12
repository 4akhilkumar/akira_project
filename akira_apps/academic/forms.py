from django import forms

class RoomTypeForm(forms.Form):
    TYPE = [
        ('Class Room','Class Room'),
        ('Staff Room','Staff Room'),
        ('Waiting Hall','Waiting Hall'),
        ('Lab','Lab'),
        ('Meeting Hall','Meeting Hall'),
    ]
    roomTypeForm = forms.ChoiceField(choices = TYPE)

class SemesterModeForm(forms.Form):
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    semesterModeForm = forms.ChoiceField(choices = MODE)