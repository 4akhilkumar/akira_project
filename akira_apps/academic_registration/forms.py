from django import forms

from akira_apps.academic_registration.models import BRANCH_CHOICES, Semester, Course

class SemesterForm(forms.Form):
    SEM_MODE = (
        ('ODD','ODD'),
        ('EVEN','EVEN'),
    )
    model = Semester
    mode = forms.ChoiceField(choices = SEM_MODE)
    fields = ['mode', 'branch', 'start_year', 'end_year']

class BranchForm(forms.Form):
    branch = forms.ChoiceField(choices = BRANCH_CHOICES)
    fields = ['branch']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"