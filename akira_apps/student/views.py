from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from django.http.response import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.contrib import messages

import secrets
import pandas as pd
import io
import csv
import datetime as pydt
import random
import string

from akira_apps.academic.models import (Branch)
from akira_apps.student.models import (Students)
from akira_apps.super_admin.forms import (BLOODGROUPForm, GENDERCHOICESForm)

@login_required(login_url=settings.LOGIN_URL)
def student_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'student/dashboard.html', context)

@login_required(login_url=settings.LOGIN_URL)
def manage_students(request):
    students = Students.objects.all()
    context = {
        "students":students,
    }
    return render(request, 'student/manage_students/manage_students.html', context)

@login_required(login_url=settings.LOGIN_URL)
def view_student(request, student_username):
    student = Students.objects.get(user__username=student_username)
    user = User.objects.get(username=student_username)
    list_groups = Group.objects.all()
    current_user_group = ', '.join(map(str, user.groups.all()))
    context = {
        "student": student,
        "current_user_group":current_user_group,
        "list_groups":list_groups,
    }
    return render(request, 'student/manage_students/view_student.html', context)

@login_required(login_url=settings.LOGIN_URL)
def students_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students_info_record' + \
        str(pydt.pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 
                    'Gender', 'Date of Birth',
                    'Blood Group', 'Door No.', 'Zip Code', 'City Name', 
                    'State Name', 'Country', 'Branch', 'Current Medical Issue', 'Designation'])
    
    students = Students.objects.all()

    for i in students:
        writer.writerow([i.user.username, i.user.first_name, i.user.last_name, i.user.email,
                        i.gender, i.date_of_birth,
                        i.blood_group, i.door_no, i.zip_code, i.city_name, 
                        i.state_name, i.country_name, i.branch, i.current_medical_issue, ', '.join(map(str, i.user.groups.all()))])
    return response

@login_required(login_url=settings.LOGIN_URL)
def bulk_upload_students_save(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['student_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password="AKIRAaccount@21",
                )
                group_name = row['Designation']
                my_group = Group.objects.get(name='%s' % str(group_name))
                my_group.user_set.add(newuser)

                student = Students.objects.bulk_create([
                    Students(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        date_of_birth=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        door_no=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        current_medical_issue=row['Current Medical Issue'],
                        blood_group=row['Blood Group'],
                        branch=row['Branch'],
                    )
                ])
        return redirect('manage_students')
    else:
        return redirect('manage_students')

@login_required(login_url=settings.LOGIN_URL)
def search_student(request):
    if request.method == 'POST':
        query = request.POST['search-student'].strip()
        beforeSearch = pydt.datetime.now()
        students = Students.objects.filter(
            Q(user__username__icontains=query) | Q(user__email__icontains=query) | Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) | Q(gender__icontains=query) |
            Q(date_of_birth__icontains=query) | Q(zip_code__icontains=query) |
            Q(city_name__icontains=query) | Q(state_name__icontains=query) |
            Q(country_name__icontains=query) | Q(current_medical_issue__icontains=query) |
            Q(blood_group__icontains=query) | Q(branch__icontains=query)
        )
        afterSearch = pydt.datetime.now()
        totalTimeTaken = (afterSearch - beforeSearch).total_seconds()
        context = {
            'students': students,
            'totalTimeTaken':totalTimeTaken,
            'query':query,
        }
        return render(request, 'student/manage_students/search_student.html', context)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_students')

def add_student(request):
    gender = GENDERCHOICESForm()
    blood_groups = BLOODGROUPForm()
    branches = Branch.objects.all()
    last_student = User.objects.filter(groups__name='Student').last()

    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(random.randint(14, 18)))
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        door_no = request.POST.get('door_no')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        blood_group = request.POST.get('blood_group')
        branch = request.POST.get('branch')
        branch = Branch.objects.get(id=branch)
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
        else:
            photo = False
        save = request.POST.get('_save')
        addanother = request.POST.get('_addanother')

        if User.objects.filter(username = username).exists() is False:
            try:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    first_name = firstname,
                    last_name = lastname
                )
                user.set_password(password)
                user.save()

                student = Students.objects.create(
                    user = user,
                    gender = gender,
                    date_of_birth = date_of_birth,
                    door_no = door_no,
                    zip_code = zip_code,
                    city = city,
                    state = state,
                    country = country,
                    blood_group = blood_group,
                    photo = photo,
                    branch = branch
                )
            except Exception as e1:
                try:
                    user.delete()
                    student.delete()
                except Exception as e2:
                    messages.error(request, str(e2))
                messages.error(request, str(e1))
                return redirect('add_student')
            if save:
                messages.success(request, "Student added successfully!")
                return redirect('manage_students')
            elif addanother:
                messages.success(request, "Student added successfully!")
                return redirect('add_student')
            else:
                messages.success(request, "Student added successfully!")
                return redirect('edit_student', stdID = user.id)
        else:
            messages.info(request, "%s already exists!" % username)
            return redirect('add_student')
    context = {
        'gender': gender,
        'blood_groups': blood_groups,
        'branches': branches,
    }
    return render(request, "student/manage_students/add_student.html", context)