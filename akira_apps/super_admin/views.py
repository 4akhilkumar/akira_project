from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from akira_apps.authentication.models import UserLoginDetails
from akira_apps.course.models import Course

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
    context = {
        "rAnd0m123":rAnd0m123,
        "listFaculty":listFaculty,
        "listStudents":listStudents,
    }
    return render(request, 'super_admin/dashboard.html', context)

@login_required(login_url=settings.LOGIN_URL)
def add_staff(request):
    form = CreateUserForm()
    staff_form = StaffsForm()
    list_groups = Group.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        staff_form = StaffsForm(request.POST,request.FILES)
        assigned_group = request.POST.get('designation-group')
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
            print(assigned_group)
            my_group = Group.objects.get(name='%s' % str(assigned_group)) 
            user = User.objects.get(id=request.user.id)
            my_group.user_set.add(user)
            print("Faculty Registered Successfully.")
            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            staff_form = StaffsForm()

    context = {
        'form':form,
        'staff_form':staff_form,
        'list_groups':list_groups,
    }       
    return render(request, 'super_admin/Staff/add_faculty.html', context)

@login_required(login_url=settings.LOGIN_URL)
def manage_staff(request):
    staffs = Staff.objects.all()
    doctorial_faculty = Staff.objects.filter(name_prefix='Dr')
    courses = Course.objects.all()
    context = {
        "staffs":staffs,
        "doctorial_faculty":doctorial_faculty,
        "courses":courses,
    }
    return render(request, 'super_admin/Staff/manage_faculty.html', context)

@login_required(login_url=settings.LOGIN_URL)
def edit_staff(request, staff_username):
    staff = Staff.objects.get(user__username=staff_username)
    form = CreateUserForm(instance=staff.user)
    staff_form = StaffsForm(instance=staff)
    list_groups = Group.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=staff.user)
        staff_form = StaffsForm(request.POST, request.FILES, instance=staff)
        assigned_group = request.POST.get('designation-group')
        if form.is_valid() and staff_form.is_valid():
            form.save()
            staff_form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            my_group = Group.objects.get(name='%s' % str(assigned_group)) 
            user = User.objects.get(id=request.user.id)
            my_group.user_set.add(user)
            print("Faculty Updated Successfully.")
            return redirect('manage_staff')
        else:
            form = CreateUserForm(instance=staff.user)
            staff_form = StaffsForm(instance=staff)

    context = {
        'form':form,
        'staff_form':staff_form,
        'list_groups':list_groups,
    }       
    return render(request, 'super_admin/Staff/edit_faculty.html', context)

@login_required(login_url=settings.LOGIN_URL)
def view_staff(request, staff_username):
    staff = Staff.objects.get(user__username=staff_username)
    user = User.objects.get(username=staff_username)
    list_groups = Group.objects.all()
    current_user_group = ', '.join(map(str, user.groups.all()))
    userLoginDetails = UserLoginDetails.objects.filter(user__username=staff_username)
    context = {
        "staff": staff,
        "current_user_group":current_user_group,
        "list_groups":list_groups,
        "userLoginDetails":userLoginDetails
    }
    return render(request, "super_admin/Staff/view_faculty.html", context)

@login_required(login_url=settings.LOGIN_URL)
def assign_user_group(request, staff_username):
    if request.method == 'POST':
        group_name = request.POST.get('designation-group')
        my_group = Group.objects.get(name='%s' % str(group_name))
        user = User.objects.get(username=staff_username) 
        my_group.user_set.remove(user)
        return redirect('manage_staff')
    else:
        return redirect('manage_staff')

@login_required(login_url=settings.LOGIN_URL)
def bulk_upload_staffs_save(request):
    if request.method == 'POST':
        staff_from_db = User.objects.all()
        staff_user=[]
        for i in staff_from_db:
            staff_user.append(i.username)
            staff_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['staff_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in staff_user and str(row['Email']) not in staff_user:
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

                staff = Staff.objects.bulk_create([
                    Staff(
                        user_id = newuser.id,
                        name_prefix=row['Name Prefix'],
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
        return redirect('manage_staff')
    else:
        return redirect('manage_staff')

import datetime as pydt
def staff_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=staff_info_record' + \
        str(pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 
                    'Name Prefix', 'Gender', 'Date of Birth',
                    'Blood Group', 'Door No.', 'Zip Code', 'City Name', 
                    'State Name', 'Country', 'Branch', 'Current Medical Issue', 'Designation'])
    
    staff = Staff.objects.all()

    for i in staff:
        writer.writerow([i.user.username, i.user.first_name, i.user.last_name, i.user.email,
                        i.name_prefix, i.gender, i.date_of_birth,
                        i.blood_group, i.door_no, i.zip_code, i.city_name, 
                        i.state_name, i.country_name, i.branch, i.current_medical_issue, ', '.join(map(str, i.user.groups.all()))])
    return response

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

# group_name = 'Staff'
# my_group = Group.objects.get(name='%s' % str(group_name))
# user = User.objects.get(id=3) 
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
# new_group, created = Group.objects.get_or_create(name ='Course Co-Ordinator')
# new_group, created = Group.objects.get_or_create(name ='Head of the Department')
# new_group, created = Group.objects.get_or_create(name ='Professor')
# new_group, created = Group.objects.get_or_create(name ='Associate Professor')
# new_group, created = Group.objects.get_or_create(name ='Assistant Professor')
# new_group, created = Group.objects.get_or_create(name ='Student')