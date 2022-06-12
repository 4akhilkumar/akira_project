from django import forms

class OpeningsJobTypeForm(forms.Form):
    JOB_TYPE_CHOICES = [
        ("", "Select Job Type"),
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
        ("Temporary", "Temporary"),
        ("Freelance", "Freelance"),
        ("Volunteer", "Volunteer"),
        ("Work From Home", "Work From Home"),
    ]
    job_type = forms.ChoiceField(choices = JOB_TYPE_CHOICES)

class GroupTypesForm(forms.Form):
    GROUP_TYPE_CHOICES = [
        ('', 'Select Group Type'),
        ('Administrator', 'Administrator'),

        ('Developer Team', 'Developer Team'),

        ('ADOPS Team', 'ADOPS Team'),
        ('EXAMS Team', 'EXAMS Team'),

        ('Applicant', 'Applicant'),
        ('Teaching Staff', 'Teaching Staff'),
        ('Non-Teaching Staff', 'Non-Teaching Staff'),
        ('Retired Staff', 'Retired Staff'),
        ('Resigned Staff', 'Resigned Staff'),

        ('Prospective Student', 'Prospective Student'),
        ('Student', 'Student'),
        ('Graduate', 'Graduate')
    ]
    group_type = forms.ChoiceField(choices = GROUP_TYPE_CHOICES)