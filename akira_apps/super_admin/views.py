from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from akira_apps.authentication.models import UserLoginDetails

from akira_apps.staff.forms import StaffsForm
from akira_apps.staff.models import Staffs
from akira_apps.authentication.forms import CreateUserForm

import secrets

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
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'super_admin/dashboard.html', context)

@login_required(login_url=settings.LOGIN_URL)
def add_staff(request):
    form = CreateUserForm()
    staff_form = StaffsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        staff_form = StaffsForm(request.POST,request.FILES)
        staff_from_db = User.objects.all()
        staff_user=[]
        for i in staff_from_db:
            staff_user.append(i.username)
            staff_user.append(i.email)
        username = request.POST.get('username')
        if username in staff_user:
            print("A user already exist with "+ username)
            return redirect('add_staff')

        if form.is_valid() and staff_form.is_valid():
            user = form.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username = username, password = password)

            group = Group.objects.get(name='Staff')
            user.groups.add(group)
            print("Faculty Registered Successfully.")
            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            staff_form = StaffsForm()

    context = {
        'form':form,
        'staff_form':staff_form
    }       
    return render(request, 'super_admin/Staff/add_faculty.html', context)

@login_required(login_url=settings.LOGIN_URL)
def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs":staffs
    }
    return render(request, 'super_admin/Staff/manage_faculty.html', context)

@login_required(login_url=settings.LOGIN_URL)
def view_staff(request, staff_id):
    staff = Staffs.objects.get(user=staff_id)
    user = User.objects.get(id=staff_id) 
    current_user_group = ', '.join(map(str, user.groups.all()))
    userLoginDetails = UserLoginDetails.objects.filter(user=staff_id)
    context = {
        "staff": staff,
        "current_user_group":current_user_group,
        "userLoginDetails":userLoginDetails
    }
    return render(request, "super_admin/Staff/view_faculty.html", context)

@login_required(login_url=settings.LOGIN_URL)
def user_group(request, staff_id):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        my_group = Group.objects.get(name='%s' % str(group_name))
        user = User.objects.get(id=staff_id) 
        my_group.user_set.add(user)
        print("Group Done")
        return redirect('manage_staff')
    else:
        return redirect('manage_staff')


# group_name = 'Student'
# group_name = 'Staff'
# group_name = 'Head of the Department'
# group_name = 'Administrator'
# group_name = 'Course Co-Ordinator'
# my_group = Group.objects.get(name='%s' % str(group_name))
# user = User.objects.get(id=5)
# my_group.user_set.add(user)
# print("Success")

# group_name = 'Staff'
# my_group = Group.objects.get(name='%s' % str(group_name))
# user = User.objects.get(id=3) 
# my_group.user_set.remove(user)
# print("Success")

# user = User.objects.get(id=2) 
# check = ', '.join(map(str, user.groups.all()))
# print(check)

new_group, created = Group.objects.get_or_create(name ='Administrator')
new_group, created = Group.objects.get_or_create(name ='Course Co-Ordinator')
new_group, created = Group.objects.get_or_create(name ='Head of the Department')
new_group, created = Group.objects.get_or_create(name ='Staff')
new_group, created = Group.objects.get_or_create(name ='Student')