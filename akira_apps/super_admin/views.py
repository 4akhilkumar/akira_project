from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from akira_apps.authentication.models import UserLoginDetails
from akira_apps.course.models import CourseMC

from akira_apps.staff.forms import StaffsForm
from akira_apps.staff.models import Staff
from akira_apps.authentication.forms import CreateUserForm

import secrets
import csv, io
import pandas as pd

from akira_apps.student.models import Students
from akira_apps.super_admin.decorators import allowed_users

def my_profile(request):
    user = User.objects.get(id=request.user.id)
    group = ', '.join(map(str, user.groups.all()))
    list_groups = Group.objects.all()
    context = {
        "user":user,
        "group":group,
        "list_groups":list_groups,
    }
    return render(request, 'super_admin/my_profile.html', context)

def save_my_profile(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.user.id)
        email = request.POST.get('email').lower()
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()

        try:
            user = User.objects.get(id=current_user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return redirect('my_profile')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request...!")

@allowed_users(allowed_roles=['Administrator'])
def assign_group(request):
    if request.method == 'POST':
        assigned_group = request.POST.getlist('group_name')
        try:
            for i in assigned_group:
                my_group = Group.objects.get(name='%s' % str(i)) 
                user = User.objects.get(id=request.user.id)
                my_group.user_set.remove(user)
            return redirect('my_profile')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request...!")

@login_required(login_url=settings.LOGIN_URL)
@allowed_users(allowed_roles=['Administrator'])
def super_admin_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    listFaculty = Staff.objects.all()
    listStudents = Students.objects.all()
    listCourses = CourseMC.objects.all()
    context = {
        "rAnd0m123":rAnd0m123,
        "listFaculty":listFaculty,
        "listStudents":listStudents,
        "listCourses":listCourses,
    }
    return render(request, 'super_admin/dashboard.html', context)

@login_required(login_url=settings.LOGIN_URL)
def assign_user_group(request, staff_username):
    if request.method == 'POST':
        group_name = request.POST.get('designation-group')
        my_group = Group.objects.get(name='%s' % str(group_name))
        user = User.objects.get(username=staff_username) 
        my_group.user_set.add(user)
        return redirect('manage_staff')
    else:
        return redirect('manage_staff')

# group_name = 'Student'
# group_name = 'Staff'
# group_name = 'Head of the Department'
# group_name = 'Course Co-Ordinator'
# group_name = 'Administrator'
# my_group = Group.objects.get(name='%s' % str(group_name))
# user = User.objects.get(username = '4akhi')
# my_group.user_set.add(user)
# print("Success")

# user = User.objects.get(id=1)
# user.first_name = 'Sai Akhil Kumar Reddy'
# user.last_name = 'N'
# user.email = '4akhilkumar@gmail.com'
# user.save()

# userI = User.objects.create_user(username='hari.vege')
# userI.first_name = 'Hari Kiran'
# userI.last_name = 'Vege'
# userI.email = '4projtest@gmail.com'
# userI.save()

# userI = User.objects.get(username='hari.vege')
# userI.set_password('AKIRAaccount@21')
# userI.save()

# group_name = 'Associate Professor'
# my_group = Group.objects.get(name='%s' % str(group_name))
# user = User.objects.get(username='4akhi') 
# my_group.user_set.remove(user)
# print("Success")

# user = User.objects.get(id=2) 
# check = ', '.join(map(str, user.groups.all()))
# print(check)

# get_user = User.objects.get(username = 'KavithaDesigar')
# print(get_user.delete())
# staff = Staff.objects.get(user=get_user)
# staff.name_prefix = 'Dr'
# staff.save()


# new_group, created = Group.objects.get_or_create(name ='Administrator')
# new_group, created = Group.objects.get_or_create(name ='Head of the Department')
# new_group, created = Group.objects.get_or_create(name ='Professor')
# new_group, created = Group.objects.get_or_create(name ='Associate Professor')
# new_group, created = Group.objects.get_or_create(name ='Assistant Professor')
# new_group, created = Group.objects.get_or_create(name ='Student')