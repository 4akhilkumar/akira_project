from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import BLOOD_GROUP_CHOICES, MOTHER_TOUNGE_CHOICES, Students, Staffs
from akira_apps.academic_registration.models import BRANCH_CHOICES

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class StaffsForm(forms.ModelForm):
    class Meta:
        model = Staffs
        blood_group = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES)
        mother_tounge = forms.ChoiceField(choices = MOTHER_TOUNGE_CHOICES)
        branch = forms.ChoiceField(choices = BRANCH_CHOICES)
        fields = ('gender','father_name','father_occ','father_phone','mother_name','mother_tounge','dob','blood_group','phone','dno_sn','zip_code','city_name','state_name','country_name','profile_pic','branch','qualification','designation')

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        blood_group = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES)
        mother_tounge = forms.ChoiceField(choices = MOTHER_TOUNGE_CHOICES)
        branch = forms.ChoiceField(choices = BRANCH_CHOICES)
        fields = ['gender','father_name','father_occ','father_phone','mother_name','mother_tounge','dob','blood_group','phone','dno_sn','zip_code','city_name','state_name','country_name','profile_pic','branch'] 