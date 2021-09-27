from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from akira_apps.staff.forms import CreateUserForm, StaffsForm
from akira_apps.staff.models import Staffs

import secrets

@login_required(login_url=settings.LOGIN_URL)
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

            group = Group.objects.get(name='Faculty')
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
    context = {
        "staff": staff,
        "id": staff_id,
    }
    return render(request, "super_admin/Staff/view_faculty.html", context)