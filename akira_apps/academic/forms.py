from django import forms
from django.db import models

class BranchForm(forms.Form):
    BRANCH_CHOICES = [
        ("","Branch Name"),
        ("Computer Science and Engineering","Computer Science and Engineering"),
        ("Aerospace/aeronautical Engineering","Aerospace/aeronautical Engineering"),
        ("Chemical Engineering","Chemical Engineering"),
        ("Civil Engineering","Civil Engineering"),
        ("Electronics and Communications Engineering","Electronics and Communications Engineering"),
        ("Electrical and Electronics Engineering","Electrical and Electronics Engineering"),
        ("Petroleum Engineering","Petroleum Engineering"),
        ("Bio Technology","Bio Technology"),
        ("Mechanical Engineering","Mechanical Engineering"),
    ]
    branch = forms.ChoiceField(choices = BRANCH_CHOICES)

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