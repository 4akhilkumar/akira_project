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
from akira_apps.super_admin.forms import (BLOODGROUPForm, GENDERCHOICESForm)

@login_required(login_url=settings.LOGIN_URL)
def student_dashboard(request):
    context = {

    }
    return render(request, 'student/dashboard.html', context)

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
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        blood_group = request.POST.get('blood_group')
        phone = request.POST.get('phone')
        door_no = request.POST.get('door_no')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        photo = request.FILES['photo']
        branch_id = request.POST.get('branch')
        branch_id = "7c9645cd-290f-4282-801d-2f96fd8735a2"
        try:
            branch = Branch.objects.get(id = branch_id)
        except Branch.DoesNotExist:
            branch = None
            return redirect('add_student')
        user = User.objects.create_user(
            username = username, email = email,
            password = password,
            first_name = firstname,
            last_name = lastname
        )
        user.is_active = True # False
        applicant_group, isCreated = Group.objects.get_or_create(name = "Student")
        try:
            Students.objects.create(user = user, gender = gender, date_of_birth = date_of_birth,
                                blood_group = blood_group, phone = phone, door_no = door_no,
                                zip_code = zip_code, city = city, district = district,
                                state = state, country = country, photo = photo, branch = branch)
            user.groups.add(Group.objects.get(name = str(applicant_group)))
            user.save()
        except Exception:
            user.delete()
    context = {
    }
    return render(request, 'student/add_student.html', context)