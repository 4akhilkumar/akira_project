from django import forms

class NAMEPREFIXForm(forms.Form):
    Name_Prefix_Choices = [
    ("","Select Name Prefix"),
    ("Dean","University Dean"),
    ("Dr","Doctor (Medical or Educator)"),
    ("Hon","Honorable"),
    ("Mr","Mister"),
    ("Mrs","Married Woman"),
    ("Ms","Single/Unmarried Women"),
    ("Prof","Professor"),
    ]
    nameprefix = forms.ChoiceField(choices = Name_Prefix_Choices)

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

class GENDERCHOICESForm(forms.Form):
    GENDER_CHOICES = [
        ("", "Select Gender"),
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    gender = forms.ChoiceField(choices = GENDER_CHOICES)