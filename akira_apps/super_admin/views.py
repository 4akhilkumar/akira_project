from ipaddress import ip_address
from django import http
from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

import requests
import secrets
import csv, io
import pandas as pd
import datetime as pydt
import re

from akira_apps.academic.models import(Academy)
from akira_apps.authentication.models import (UserLoginDetails)
from akira_apps.authentication.token import (account_activation_token)
from akira_apps.course.models import CourseMC
from akira_apps.staff.models import (Staff)
from akira_apps.student.models import Students
from akira_apps.super_admin.forms import (GENDERCHOICESForm, NAMEPREFIXForm)
from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.super_admin.models import (MailLog, AdminAccountVerificationStatus)

class Date:
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.y = y

# To store number of days in all months from
# January to Dec.
monthDays = [31, 28, 31, 30, 31, 30,
			31, 31, 30, 31, 30, 31]

# This function counts number of leap years
# before the given date
def countLeapYears(d):

	years = d.y

	# Check if the current year needs to be considered
	# for the count of leap years or not
	if (d.m <= 2):
		years -= 1

	# An year is a leap year if it is a multiple of 4,
	# multiple of 400 and not a multiple of 100.
	return int(years / 4) - int(years / 100) + int(years / 400)


# This function returns number of days between two
# given dates
def getDifference(dt1, dt2):

	# COUNT TOTAL NUMBER OF DAYS BEFORE FIRST DATE 'dt1'

	# initialize count using years and day
	n1 = dt1.y * 365 + dt1.d

	# Add days for months in given date
	for i in range(0, dt1.m - 1):
		n1 += monthDays[i]

	# Since every leap year is of 366 days,
	# Add a day for every leap year
	n1 += countLeapYears(dt1)

	# SIMILARLY, COUNT TOTAL NUMBER OF DAYS BEFORE 'dt2'

	n2 = dt2.y * 365 + dt2.d
	for i in range(0, dt2.m - 1):
		n2 += monthDays[i]
	n2 += countLeapYears(dt2)

	# return difference between two counts
	return (n2 - n1)

def validateUserDOB(dob):
    inputDate = str(dob)
    success_msg = ""
    error_msg = ""
    # Check whether the inputDate is in "YYYY-MM-DD" format or not using regex pattern and check year, month and day are valid or not
    if re.match("^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", inputDate):
        isinputDateValid = True
    else:
        isinputDateValid = False

    if isinputDateValid is True:
        dob = str(inputDate)
        split_space = dob.split(' ')
        yyyy, mm, dd = map(int, split_space[0].split('-'))

        dt1 = Date(dd, mm, yyyy)

        today = str(pydt.datetime.today())
        split_space = today.split(' ')
        present_yyyy, present_mm, present_dd = map(int, split_space[0].split('-'))

        dt2 = Date(present_dd, present_mm, present_yyyy)

        totaldiff = getDifference(dt1, dt2)
        years = int(totaldiff/365)
        if years >= 18:
            success_msg = True
        else:
            error_msg = "False"
    else:
        error_msg = ("%s is not in YYYY-MM-DD format" % format(inputDate))
    return [success_msg, error_msg]

def adminInstituteRegistration(request):
    name_prefix_list = NAMEPREFIXForm()
    gender_list = GENDERCHOICESForm()
    if request.method == 'POST':
        firstname = request.POST.get('firstname').title()
        lastname = request.POST.get('lastname').title()
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email').lower()
        phone = request.POST.get('phone')

        nameprefix = request.POST.get('name_prefix')
        dob = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')

        doorno = request.POST.get('door_no')
        zipcode = request.POST.get('zip_code')
        city = request.POST.get('city') or request.POST.get('new_city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')

        photo = request.FILES.get('photo')

        institutecode = request.POST.get('institute_code')
        institutename = request.POST.get('institute_name').title()
        instituteaddress = request.POST.get('institute_address')

        if User.objects.filter(groups__name = "Administrator", is_staff = True, is_active = True, is_superuser = True).exists() is True:
            messages.info(request, "Administrator & Institute already registered")
            return redirect('login')

        # # convert the request.POST to dict
        # request_dict = request.POST.dict()
        # print(all(request_dict))
        # print(request_dict)

        validatedUserDOB = validateUserDOB(dob)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            url = 'https://akira-rest-api.herokuapp.com/getEmail/{}/?format=json'.format(email)
            response = requests.get(url)
            dataEmail = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")
            return redirect('adminInstituteRegistration')

        if validatedUserDOB[0] is True:
            if dataEmail['ValidEmail'] is True and dataEmail['Disposable'] is False:
                if not User.objects.filter(username=username).exists():
                    if password == confirm_password:
                        user = User.objects.create_superuser(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                        admin_group, isCreated = Group.objects.get_or_create(name ='Administrator')
                        user.groups.add(Group.objects.get(name = str(admin_group)))
                        user.is_active = False
                        user.is_staff = False
                        user.is_superuser = False
                        user.save()
                        Staff.objects.create(
                            user = user, name_prefix = nameprefix, date_of_birth = dob, gender = gender, phone = phone,
                            door_no = doorno, zip_code = zipcode, city = city, district = district, state = state, country = country,
                            photo = photo)
                        Academy.objects.create(user=user, code=institutecode, name=institutename, address=instituteaddress)
                        AdminAccountVerificationStatus.objects.create(user=user, verificationStatus = False, ipaddress = ip)
                        try:
                            url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
                            response = requests.get(url)
                            dataUsername = response.json()
                        except Exception:
                            messages.info(request, "Server under maintenance. Please try again later.")
                            return redirect('adminInstituteRegistration')
                        return redirect('send_admin_reg_email', EnUsername = dataUsername['EncryptedUsername'])
                    else:
                        messages.info(request, "Password didn't Match")
                        return redirect('adminInstituteRegistration')
                else:
                    messages.error(request, "Username Already Exists...!")
                    return redirect('adminInstituteRegistration')
            elif dataEmail['Disposable'] is True:
                messages.error(request, "Don't use disposable email address")
                return redirect('adminInstituteRegistration')
            else:
                messages.error(request, "Please use legitimate email address only")
                return redirect('adminInstituteRegistration')
        elif "not in YYYY-MM-DD format" in validatedUserDOB[1] :
            messages.error(request, str(validatedUserDOB[1]))
            return redirect('adminInstituteRegistration')
        elif validatedUserDOB[1] == "False":
            notice_context2 = {
                'title': 'Not Eligible',
                'message': 'You are not eligible to register as a Admininstrator',
            }
            return render(request, 'notice.html', notice_context2)
    context = {
        'name_prefix': name_prefix_list,
        'gender': gender_list,
    }
    return render(request, "super_admin/register.html", context)

def send_admin_reg_email(request, EnUsername):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('adminInstituteRegistration')
    
    isMailSent = False
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except Exception as e:
        messages.error(request, str(e))
        return redirect('adminInstituteRegistration')

    if User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = False, is_staff = False, is_superuser = False).exists() is True:        
        ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=10)
        if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your registration - AkirA", created_at__gte=ten_minutes_ago).exists() is False:
            try:
                current_site = get_current_site(request)
                protocol = request.is_secure() and "https" or "http"
                mail_subject = "Confirm your registration - AkirA"
                message = render_to_string('super_admin/verify_admin_email.html', {
                    'user': user,
                    'protocol': protocol,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(EnUsername)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user.email
                send_mail(
                    subject = mail_subject,
                    message=None,
                    html_message = message,
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [to_email],
                    fail_silently = False,
                )
                isMailSent = True
                if isMailSent is True:
                    MailLog.objects.create(user=user, subject = mail_subject)
                    messages.success(request, "Confirmation email sent!")
                else:
                    messages.error(request, "Unable to send confirmation email!")
                return redirect("waitingAdminConfirm", EnUsername = EnUsername)
            except Exception as e1:
                isMailSent = False
                messages.error(request, str(e1))
                return redirect("waitingAdminConfirm", EnUsername = EnUsername)
        else:
            messages.error(request, "You can't request confirm email within 10 minutes")
            return redirect("waitingAdminConfirm", EnUsername = EnUsername)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def waitingAdminConfirm(request, EnUsername):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('adminInstituteRegistration')
    ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=1000)
    last_mail_time = ''
    if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your registration - AkirA", created_at__gte=ten_minutes_ago).exists() is True:
        getlast_mail_time = MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your registration - AkirA", created_at__gte=ten_minutes_ago)
        lastObject = getlast_mail_time.last()
        last_mail_time = lastObject.created_at
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return redirect('adminInstituteRegistration')
    if user.is_active is False:
        notice_context = {
            'EnUsername': EnUsername,
            'last_mail_time': last_mail_time,
        }
        return render(request, 'super_admin/waitingAdminConfirm.html', notice_context)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def confirm_admin_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        try:
            url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(uid)
            response = requests.get(url)
            dataUsername = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")
            return redirect('login')
        user = User.objects.get(username=dataUsername['DecryptedUsername'])
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        updateAAVS = AdminAccountVerificationStatus.objects.get(user=user)
        updateAAVS.verificationStatus = True
        updateAAVS.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        return HttpResponse(status = 404)

def isAdminRegConfirmed(request):
    if request.method == 'POST':
        uid = request.POST.get('bfpID')
        EnUsername = request.POST.get('EnUsername')
        try:
            url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(EnUsername)
            response = requests.get(url)
            dataUsername = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        dataResponse = {
                'status': 'failed',
        }
        isAdminAccountCreated = User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = True, is_staff = True, is_superuser = True).exists()
        if isAdminAccountCreated is True:
            print("Here0")
            try:
                getAAVIPAddr = AdminAccountVerificationStatus.objects.get(user__username = dataUsername['DecryptedUsername'])
                print("Here1")
            except Exception:
                getAAVIPAddr = None
                print("Here2")
            if str(ip) == str(getAAVIPAddr.ipaddress) or str(uid) == str(getAAVIPAddr.bfpID):
                print("Here3")
                dataResponse = {
                    'status': 'success',
                }
                print("Here4")
            print("Here5")
        print("Here6")
        print(dataResponse)
        return JsonResponse(dataResponse)

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

# new_group, created = Group.objects.get_or_create(name ='Administrator')
# new_group, created = Group.objects.get_or_create(name ='Head of the Department')
# new_group, created = Group.objects.get_or_create(name ='Professor')
# new_group, created = Group.objects.get_or_create(name ='Associate Professor')
# new_group, created = Group.objects.get_or_create(name ='Assistant Professor')
# new_group, created = Group.objects.get_or_create(name ='Student')

# if User.objects.filter(username='4akhilkumar').exists() is True:
#     user = User.objects.get(username = '4akhilkumar')
# else:
#     user = User.objects.create_user(username='4akhilkumar')
# user.username = '4akhilkumar'
# user.first_name = 'Sai Akhil Kumar Reddy'
# user.last_name = 'N'
# user.email = '4akhilkumar@gmail.com'
# user.set_password("AKIRAaccount@21")
# user.is_active = True
# user.is_staff = True
# user.is_superuser = True
# user.save()

# group_name = 'Administrator'
# my_group = Group.objects.get(name='%s' % str(group_name))
# my_group.user_set.add(user)
# print("Success")

# my_group = Group.objects.get(name='%s' % str(group_name))
# my_group.user_set.remove(user)
# print("Success")