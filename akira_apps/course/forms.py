from django import forms

class CourseTypeForm(forms.Form):
    COURSE_TYPE = [
        ("", "Course Type"),
        ("Professional Elective", "Professional Elective"),
        ("Foreign Language Elective", "Foreign Language Elective"),
        ("Open Elective", "Open Elective"),
        ("Science Elective", "Science Elective"),
        ("NDY", "NDY"),
    ]
    type = forms.ChoiceField(choices = COURSE_TYPE)

class CourseExtraFieldForm(forms.Form):
    FIELD_TYPE = [
        ("", "Select Field type"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("number", "Number"),
    ]
    fieldtype = forms.ChoiceField(choices = FIELD_TYPE)