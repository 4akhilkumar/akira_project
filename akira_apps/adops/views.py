from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
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

from akira_apps.academic.models import (Academy)
from akira_apps.adops.forms import (OpeningsJobTypeForm, ExtraFieldValueTypeForm)
from akira_apps.adops.models import (Openings)
from akira_apps.authentication.token import (account_activation_token)
from akira_apps.staff.models import (Staff)
from akira_apps.super_admin.forms import (GENDERCHOICESForm, NAMEPREFIXForm)
from akira_apps.super_admin.models import (MailLog)
from akira_apps.staff.models import (Skills)

def manage_adops(request):
    openings = Openings.objects.all()
    applied_openings = Openings.objects.filter(applied__isnull=False).distinct()
    applied_openings_count = Openings.objects.filter(applied__isnull=False)
    context = {
        'openings': openings,
        'applied_openings': applied_openings,
        'applied_openings_count': applied_openings_count,
    }
    return render(request, 'adops/manage_adops.html', context)

def openings(request):
    try:
        academy = Academy.objects.all()[0]
    except Exception as e:
        academy = None
    openings = Openings.objects.all().order_by('-created_at')
    is_admin = request.user.groups.filter(name='Administrator').exists()
    if request.method == "POST":
        if request.user.is_authenticated:
            job_id = request.POST.get('job_id')
            if Openings.objects.filter(id = job_id).exists():
                if Openings.objects.filter(id = job_id, applied = request.user).exists():
                    messages.warning(request, "You have already applied for this opening!")
                elif Openings.objects.filter(applied = request.user).exists():
                    messages.info(request, "You can apply only for one opening!")
                else:
                    appliedOpening = Openings.objects.get(id = job_id)
                    appliedOpening.applied.add(request.user)
                    messages.success(request, "You have successfully applied for this opening!")
                return redirect('openings')
            else:
                messages.error(request, "Opening doesn't exist!")
                return redirect('openings')
        else:
            messages.info(request, "You must be logged in to apply for an opening")
            return redirect('applicantsAccount')

    context = {
        'academy': academy,
        'openings': openings,
        'is_admin': is_admin,
    }
    return render(request, 'adops/openings/apply_opening.html', context)

def add_openings(request):
    contact_person = User.objects.filter(groups__name='Administrator')
    job_type_list = OpeningsJobTypeForm()
    extra_field_value_type_list = ExtraFieldValueTypeForm()
    if request.method == "POST":
        job = request.POST.get('job')
        overview = request.POST.get('overview').strip()
        description = request.POST.get('description').strip()
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        location = request.POST.get('location')
        pay_scale = request.POST.get('pay_scale')
        job_type = request.POST.get('job_type')
        contact_person = request.POST.get('contact_person')
        if User.objects.filter(id=contact_person).exists():
            contact_person = User.objects.get(id=contact_person)
        else:
            messages.error(request, "Contact Person doesn't exist")
            return redirect('add_opening')

        try:
            Openings.objects.create(
                job=job,
                overview=overview,
                description=description,
                experience=experience,
                qualification=qualification,
                location=location,
                pay_scale=pay_scale,
                type = job_type,
                contact_person=contact_person
            )
            messages.success(request, 'Opening created successfully')
        except Exception as e:
            if "Duplicate entry" in str(e):
                messages.error(request, "Opening already exists!")
            else:
                messages.error(request, str(e))
        return redirect('add_openings')
    context = {
        'contact_person': contact_person,
        'job_type_list':job_type_list,
        'extra_field_value_type_list':extra_field_value_type_list,
    }
    return render(request, 'adops/openings/add_opening.html', context)

# def draft_opening_Ajax(request):
#     data_error = None
#     object_status = None
#     openingObj = None
#     if request.is_ajax and request.method == "POST":
#         job = request.POST.get('job')
#         description = request.POST.get('description').strip()
#         min_experience = request.POST.get('min_experience')
#         if request.POST.get('max_experience'):
#             max_experience = request.POST.get('max_experience')
#         else:
#             max_experience = None
#         qualification = request.POST.get('qualification')
#         location = request.POST.get('location')
#         pay_scale = request.POST.get('pay_scale')
#         job_type = request.POST.get('job_type')
#         contact_person = request.POST.get('contact_person')
#         if User.objects.filter(id=contact_person).exists():
#             contact_person = User.objects.get(id=contact_person)
#         else:
#             data_error = False # Doesn't Exists

#         try:
#             openingObj = Openings.objects.create(
#                 job=job,
#                 description=description,
#                 min_experience=min_experience,
#                 max_experience=max_experience,
#                 qualification=qualification,
#                 location=location,
#                 pay_scale=pay_scale,
#                 type = job_type,
#                 contact_person=contact_person
#             )
#             object_status = True
#         except Exception:
#             object_status = False
#         data = {
#             'object_status': object_status,
#             'data_error': data_error,
#             'openingObj': openingObj.id,
#         }
#         response = JsonResponse(data)
#         return response

def editOpening(request, openingID):
    contact_person = User.objects.filter(groups__name='Administrator')
    job_type_list = OpeningsJobTypeForm()
    try:
        openingIDObj = Openings.objects.get(id=openingID)
    except Exception:
        messages.error(request, "Opening doesn't exist!")
        return redirect('openings')
    if request.method == "POST":
        job = request.POST.get('job')
        overview = request.POST.get('overview').strip()
        description = request.POST.get('description').strip()
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        location = request.POST.get('location')
        pay_scale = request.POST.get('pay_scale')
        job_type = request.POST.get('job_type')
        contact_person = request.POST.get('contact_person')
        if User.objects.filter(id=contact_person).exists():
            contact_person = User.objects.get(id=contact_person)
        else:
            messages.error(request, "Contact Person doesn't exist")
            return redirect('add_opening')

        try:
            openingObj = Openings.objects.filter(id = openingID).update(
                job=job,
                overview=overview,
                description=description,
                experience=experience,
                qualification=qualification,
                location=location,
                pay_scale=pay_scale,
                type = job_type,
                contact_person=contact_person
            )
            messages.success(request, 'Opening updated successfully')
        except Exception as e:
            if "Duplicate entry" in str(e):
                messages.error(request, "Opening already exists!")
            else:
                messages.error(request, str(e))
        return redirect('openings')
    context = {
        'openingIDObj': openingIDObj,
        'contact_person': contact_person,
        'job_type_list':job_type_list,
    }
    return render(request, 'adops/openings/edit_opening.html', context)

def deleteOpening(request, openingID):
    try:
        Openings.object.get(id = openingID).delete()
        messages.success(request, "Opening deleted")
    except Exception:
        messages.error(request, "Failed to delete the opening!")
    return redirect('add_openings')

def fetch_each_opening_Ajax(request):
    if request.method == "POST":
        opening_id = request.POST['openingID']
        try:
            openingObj = Openings.objects.filter(id = opening_id)
        except Exception as e:
            print(e)
        return JsonResponse(list(
            openingObj.values(
                'id', 'job',
                'overview',
                'description',
                'experience', 'qualification',
                'location', 'pay_scale',
                'type', 'contact_person',
                'applied',
                'created_at'
                )), safe = False)

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

def applicantsAccount(request):
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
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')

        photo = request.FILES.get('photo')
        resume = request.FILES.get('resume')

        validatedUserDOB = validateUserDOB(dob)

        if validatedUserDOB[0] is True:
            if not User.objects.filter(username=username).exists():
                if password == confirm_password:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                    applicant_group, isCreated = Group.objects.get_or_create(name ='Applicant')
                    user.groups.add(Group.objects.get(name = str(applicant_group)))
                    user.is_active = False
                    user.is_staff = False
                    user.save()
                    Staff.objects.create(
                        user = user, name_prefix = nameprefix, date_of_birth = dob, gender = gender, phone = phone,
                        door_no = doorno, zip_code = zipcode, city = city, district = district, state = state, country = country,
                        photo = photo, resume = resume)
                    about_receiveing_email = "If you didn't recieve any email, please check your spam folder \
                                                            or change your internet connection"
                    try:
                        current_user = User.objects.get(username = user.username)
                        try:
                            url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
                            response = requests.get(url)
                            dataUsername = response.json()
                        except Exception:
                            messages.info(request, "Server under maintenance. Please try again later.")
                            return redirect('applicantsAccount')
                        EncryptedUsername = dataUsername['EncryptedUsername']
                        current_site = get_current_site(request)
                        protocol = request.is_secure() and "https" or "http"
                        mail_subject = "Confirm your applicant registration - AkirA"
                        message = render_to_string('adops/openings/verify_applicant_email.html', {
                            'user': user,
                            'protocol': protocol,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(EncryptedUsername)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = current_user.email
                        email = EmailMessage(mail_subject, message, to=[to_email])
                        email.send()
                        messages.info(request, "Please check you email inbox")
                        MailLog.objects.create(user=current_user, subject = mail_subject)
                        messages.success(request, "Registration Successful...!")
                    except Exception as e1:
                        messages.error(request, str(e1))
                    notice_context1 = {
                        'title': 'Registration confirmation is pending',
                        'message': about_receiveing_email,
                        'send_mail_again': True,
                        'username': user.username,
                        'user_type': 'applicant',
                    }
                    return render(request, 'notice.html', notice_context1)
                else:
                    messages.info(request, "Password Didn't Match")
                    return redirect('applicantsAccount')
            else:
                messages.error(request, "Username Already Exists...!")
                return redirect('applicantsAccount')
        elif "not in YYYY-MM-DD format" in validatedUserDOB[1] :
            messages.error(request, str(validatedUserDOB[1]))
            return redirect('applicantsAccount')
    context = {
        'name_prefix': name_prefix_list,
        'gender': gender_list,
    }
    return render(request, 'adops/openings/register_applicant.html', context)

def send_applicant_reg_email_again(request, username):
    try:
        user = User.objects.get(username = username)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('applicantsAccount')
    get_last_mail_sent = MailLog.objects.filter(user__username = username, subject = "Confirm your applicant registration - AkirA").order_by('-created_at')[0]
    last_mail_time = get_last_mail_sent.created_at
    current_time = pydt.datetime.now()
    difference = current_time - last_mail_time
    difference_in_minutes = int(difference.seconds / 60)
    if User.objects.filter(username = username, is_active = False, is_staff = False).exists() is True:
        about_receiveing_email = "If you didn't recieve any email, please check your spam folder \
                                    or change your internet connection"
        if difference_in_minutes > 10:
            try:
                try:
                    url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
                    response = requests.get(url)
                    dataUsername = response.json()
                except Exception:
                    messages.info(request, "Server under maintenance. Please try again later.")
                    return redirect('applicantsAccount')
                EncryptedUsername = dataUsername['EncryptedUsername']
                current_site = get_current_site(request)
                protocol = request.is_secure() and "https" or "http"
                mail_subject = "Confirm your applicant registration - AkirA"
                message = render_to_string('adops/openings/verify_applicant_email.html', {
                    'user': user,
                    'protocol': protocol,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(EncryptedUsername)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user.email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                MailLog.objects.create(user=user, subject = mail_subject)
                messages.success(request, "Email has been sent again")
            except Exception as e1:
                messages.error(request, str(e1))
        else:
            messages.error(request, "You can't send mail again within 10 minutes")
        notice_context = {
            'title': 'Registration confirmation is pending',
            'message': about_receiveing_email,
            'send_mail_again': True,
            'username': user.username,
            'user_type': 'applicant',
        }
        return render(request, 'notice.html', notice_context)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def confirm_applicant_email(request, uidb64, token):
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
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        return HttpResponse(status = 404)

def userAppliedOpenings(request):
    currentUser = request.user
    appliedOpenings = Openings.objects.filter(applied = currentUser)
    context = {
        'appliedOpenings':appliedOpenings,
    }
    return render(request, 'adops/openings/openingsAppliedInfo.html', context)

def withdrawAppl(request, openingID):
    if Openings.objects.filter(id = openingID).exists() is True:
        currentUser = request.user
        if Openings.objects.filter(id = openingID, applied = currentUser).exists() is True:
            appliedOpening = Openings.objects.get(id = openingID)
            appliedOpening.applied.remove(currentUser)
            messages.info(request, "Your application is withdrawn")
        else:
            messages.error(request, "You haven't applied for this opening!")
        return redirect('userAppliedOpenings')
    else:
        return redirect('userAppliedOpenings')
    
def applicantsInfo(request, openingID):
    if Openings.objects.filter(id = openingID, applied__isnull=False).exists() is True:
        openingApplicants = Openings.objects.get(id = openingID)
        applicants = openingApplicants.applied.all()
        for eachApplicant in applicants:
            userID = eachApplicant.id
            if User.objects.filter(id = userID).exists() is True:
                userObj = User.objects.get(id = userID)
                if Staff.objects.filter(user = userObj).exists() is True:
                    context = {
                        'openingApplicants': openingApplicants,
                        'applicants':applicants,
                    }
                    return render(request, 'adops/openings/applicantsInfo.html', context)
                else:
                    messages.error(request, "Applicant doesn't exist!")
                    return redirect('userAppliedOpenings')
            else:
                messages.error(request, "User doesn't exist!")
                return redirect('userAppliedOpenings')
    else:
        messages.info(request, "No applicants for this opening")
        return redirect('userAppliedOpenings')

def profile(request):
    currentUser = request.user
    if User.objects.filter(id = currentUser.id).exists() is True:
        userObj = User.objects.get(id = currentUser.id)
        try:
            staff = Staff.objects.get(user = userObj)
        except Exception.ObjectDoesNotExist:
            staff = None
        if request.method == "POST":
            skills_list = request.POST.get('skills')
            photo = request.FILES.get('photo')
            print(photo)
            about = request.POST.get('about').strip()
            if about == '':
                about = None
            skills_list = skills_list.split(',')
            staff.about = about
            staff.photo = photo
            staff.save()
            for eachskill in skills_list:
                eachskill = eachskill.strip()
                if Skills.objects.filter(name = eachskill).exists() is False:
                    skillObj = Skills.objects.create(name = eachskill)
                    if staff.skills.filter(name = eachskill).exists() is False:
                        staff.skills.add(skillObj)
                    else:
                        messages.info(request, "You already have this skill!")
                else:
                    skillObj = Skills.objects.get(name = eachskill)
                    if staff.skills.filter(name = eachskill).exists() is False:
                        staff.skills.add(skillObj)
                    else:
                        messages.info(request, "You already have this skill!")
            return redirect('profile')
        context = {
            'staff': staff,
            'userObj': userObj,
        }
        return render(request, 'adops/userprofile.html', context)
    else:
        messages.error(request, "User doesn't exist!")
        return redirect('login')

def fetch_each_applicant_Ajax(request):
    if request.method == "POST":
        userID = request.POST.get('applID')
        try:
            userObj = User.objects.get(id = userID)
            staffObj = Staff.objects.filter(user = userObj)
        except Exception as e:
            print(e)
        return JsonResponse(list(
            staffObj.values(
                'id',
                'user__first_name',
                'user__last_name',
                'user__email',
                'name_prefix',
                'gender', 'date_of_birth',
                'blood_group', 'phone',
                'door_no', 'zip_code',
                'city', 'district',
                'state', 'country',
                'skills', 'about'
                )), safe = False)