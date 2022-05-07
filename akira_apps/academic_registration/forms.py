from django import forms

class SemesterModeForm(forms.Form):
    MODE = [
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    ]
    semesterModeForm = forms.ChoiceField(choices = MODE)