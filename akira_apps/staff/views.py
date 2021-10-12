import io
from os import error
from django.contrib.auth import authenticate
from django.http import request
from django.http.response import HttpResponse
import pandas as pd

from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

from akira_apps.academic_registration.forms import BranchForm, CourseForm
from akira_apps.super_admin.decorators import allowed_users
from akira_apps.authentication.forms import CreateUserForm
from akira_apps.academic_registration.models import Course, Semester
from akira_apps.staff.models import Staffs
from akira_apps.student.forms import StudentsForm
from akira_apps.student.models import Students

import secrets

@allowed_users(allowed_roles=['Staff'])
def staff_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/staff_dashboard.html', context)

@allowed_users(allowed_roles=['Course Co-Ordinator'])
def cc_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/cc_dashboard.html', context)

@allowed_users(allowed_roles=['Head of the Department'])
def hod_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/hod_templates/hod_dashboard.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_courses(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    if Semester.objects.all().count() == 0:
        return redirect('create_semester')
    elif Staffs.objects.all().count() == 0:
        return redirect('add_staff')

    course_coordinator_list = User.objects.filter(groups__name='Administrator')
    branch_list = BranchForm()
    semester_list = Semester.objects.all()

    context = {
        "rAnd0m123":rAnd0m123,
        "course_coordinator_list":course_coordinator_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
    }
    return render(request, 'staff/hod_templates/courses_templates/create_courses.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def save_created_course(request):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseShortInfo = request.POST.get('course_short_info')
        courseWywl = request.POST.get('course_wywl')
        courseSywg = request.POST.get('course_sywg')
        courseDesc = request.POST['course_desc']
        courseCoOrdinator = request.POST.get('course_coordinator')
        courseCoOrdinator_id = User.objects.get(id=courseCoOrdinator)
        branch_name = request.POST.get('branch')
        semester_info = request.POST.get('semester')
        semester_id = Semester.objects.get(id=semester_info)

        try:
            course = Course(course_code=courseCode, 
                            course_name=courseName, 
                            course_short_info=courseShortInfo, 
                            course_wywl=courseWywl, 
                            course_sywg=courseSywg, 
                            course_desc=courseDesc, 
                            course_coordinator=courseCoOrdinator_id, 
                            branch=branch_name, 
                            semester=semester_id)
            course.save()
            return redirect('manage_courses')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def edit_course(request, course_id):
    rAnd0m123 = secrets.token_urlsafe(16)
    course = Course.objects.get(id=course_id)
    course_coordinator_list = User.objects.filter(groups__name='Administrator')
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    context = {
        "rAnd0m123":rAnd0m123,
        "course":course,
        "course_coordinator_list":course_coordinator_list,
        "branch_list":branch_list,
        "semester_list":semester_list
    }
    return render(request, 'staff/hod_templates/courses_templates/edit_course.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def save_edit_course(request, course_id):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseShortInfo = request.POST.get('course_short_info')
        courseWywl = request.POST.get('course_wywl')
        courseSywg = request.POST.get('course_sywg')
        courseDesc = request.POST['course_desc']
        courseCoOrdinator = request.POST.get('course_coordinator')
        courseCoOrdinator_id = User.objects.get(id=courseCoOrdinator)
        branch_name = request.POST.get('branch')
        semester_info = request.POST.get('semester')
        semester_id = Semester.objects.get(id=semester_info)

        try:
            course = Course.objects.get(id=course_id)
            course.course_code=courseCode
            course.course_name=courseName
            course.course_short_info=courseShortInfo
            course.course_wywl=courseWywl
            course.course_sywg=courseSywg
            course.course_desc=courseDesc
            course.course_coordinator=courseCoOrdinator_id
            course.branch=branch_name
            course.semester=semester_id
            course.save()
            return redirect('manage_courses')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_courses(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('manage_courses')

def manage_courses(request):
    list_courses = Course.objects.all()
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all()))
    print(group_list)
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
        "list_courses":list_courses,
        "group_list":group_list
    }
    return render(request, 'staff/hod_templates/courses_templates/manage_courses.html', context)

def view_courses(request, course_id):
    view_course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all()))
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
        "view_course":view_course,
        "group_list":group_list
    }
    return render(request, 'staff/hod_templates/courses_templates/view_course.html', context)

@allowed_users(allowed_roles=['Administrator'])
def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST,request.FILES)
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)
        username = request.POST.get('username')
        if username in student_user:
            print("A user already exist with "+ username)
            return redirect('add_student')

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username = username, password = password)

            group = Group.objects.get(name='Student')
            user.groups.add(group)
            print("Student Registered Successfully.")
            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            student_form = StudentsForm()

    context = {'form':form, 'student_form':student_form}        
    return render(request, 'staff/admission_templates/add_student.html', context)

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