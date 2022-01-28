from django import forms

class BLOODGROUPForm(forms.Form):
    BLOOD_GROUP_CHOICES = [
    ("","Blood Group"),
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("O+","O+"),
    ("O-","O-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
    ]
    bloodgroup = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES)