import io
from os import error
import pandas as pd

from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

from .forms import CreateUserForm, StudentsForm, CourseForm
from akira_apps.student.models import Students
from .models import Course

import secrets

# Create your views here.
def staff_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/staff_dashboard.html', context)

def cc_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/cc_dashboard.html', context)

def hod_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/hod_templates/hod_dashboard.html', context)

def create_courses(request):
    try:
        form = CourseForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    except Exception as e:
        print(e)

    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
        "form":form
    }
    return render(request, 'staff/hod_templates/courses_templates/create_courses.html', context)

def update_courses(request):

    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123
    }
    return render(request, 'staff/hod_templates/update_courses.html', context)

def delete_courses(request):

    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123
    }
    return render(request, 'staff/hod_templates/courses.html', context)

def manage_courses(request):
    list_courses = Course.objects.all()
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
        "list_courses":list_courses
    }
    return render(request, 'staff/hod_templates/courses_templates/manage_courses.html', context)

def view_courses(request, course_id):
    view_course = Course.objects.get(id=course_id)
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
        "view_course":view_course
    }
    return render(request, 'staff/hod_templates/courses_templates/view_course.html', context)

def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST,request.FILES)

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = AuthenticationForm(username = username, password = password)

            group = Group.objects.get(name='Student')
            user.groups.add(group)

            return redirect('manage_student')
        else:
            form = CreateUserForm()
            student_form = StudentsForm()

    context = {'form':form, 'student_form':student_form}        
    return render(request, "oncl_app/admin_templates/student_templates/add_student.html", context)

def bulk_upload_students_save(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['studentfile'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password=row['Password'],
                )
                Student=Group.objects.get(name='Student')
                if row['Group'] == 'Student':
                    Student.user_set.add(newuser)
                    newuser.groups.add(Student)

                student = Students.objects.bulk_create([
                    Students(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        father_name=row['Father Name'],
                        father_occ=row['Father Occupation'],
                        father_phone=row['Father Phone'],
                        mother_name=row['Mother Name'],
                        mother_tounge=row['Mother Tounge'],
                        dob=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        blood_group=row['Blood Group'],
                        phone=row['Phone'],
                        dno_sn=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        branch=row['Branch']
                    )
                ])
        success_message = "Student Record(s) Imported Successfully."
        context = {
            "success_message":success_message
        }
        return redirect('manage_student', context)
    else:
        error_message = "Failed to Import Bulk Records!."
        context = {
            "error_message":error_message
        }
        return redirect('manage_student', context)