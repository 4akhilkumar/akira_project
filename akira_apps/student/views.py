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
from datetime import datetime

from akira_apps.authentication.models import UserLoginDetails
from akira_apps.student.models import Students

@login_required
def student_dashboard(request):
    previous_user_login_details = UserLoginDetails.objects.filter(user__username = request.user)
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "previous_user_login_details":previous_user_login_details,
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def manage_students(request):
    students = Students.objects.all()
    context = {
        "students":students,
    }
    return render(request, 'student/manage_students/manage_students.html', context)

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

def students_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students_info_record' + \
        str(pydt.datetime.now()) + '.csv'

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
        beforeSearch = datetime.now()
        students = Students.objects.filter(
            Q(user__username__icontains=query) | Q(user__email__icontains=query) | Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) | Q(gender__icontains=query) |
            Q(date_of_birth__icontains=query) | Q(zip_code__icontains=query) |
            Q(city_name__icontains=query) | Q(state_name__icontains=query) |
            Q(country_name__icontains=query) | Q(current_medical_issue__icontains=query) |
            Q(blood_group__icontains=query) | Q(branch__icontains=query)
        )
        afterSearch = datetime.now()
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