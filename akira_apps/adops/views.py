from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

import requests
import datetime as pydt
import re

from akira_apps.academic.models import (Academy, Branch)
from akira_apps.adops.forms import (OpeningsJobTypeForm)
from akira_apps.adops.models import (UserProfile, Admission, Openings, Programme, AdmissionRegister, StuAdmAccountVerificationStatus)
from akira_apps.authentication.token import (account_activation_token)
from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.super_admin.forms import (GENDERCHOICESForm, NAMEPREFIXForm)
from akira_apps.super_admin.models import (MailLog)

@allowed_users(allowed_roles=['Administrator', 'Adops Team'])
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

@allowed_users(allowed_roles=['Administrator', 'Adops Team'])
def add_openings(request):
    contact_person = User.objects.filter(groups__name='Administrator')
    job_type_list = OpeningsJobTypeForm()
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
                print(e)
            return redirect('add_openings')
        return redirect('manage_adops')
    context = {
        'contact_person': contact_person,
        'job_type_list':job_type_list
    }
    return render(request, 'adops/openings/add_opening.html', context)

@allowed_users(allowed_roles=['Administrator', 'Adops Team'])
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
            Openings.objects.filter(id = openingID).update(
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
            messages.error(request, str(e))
            return redirect('editOpening', editOpening = openingID )
        return redirect('openings')
    context = {
        'openingIDObj': openingIDObj,
        'contact_person': contact_person,
        'job_type_list':job_type_list,
    }
    return render(request, 'adops/openings/edit_opening.html', context)

@allowed_users(allowed_roles=['Administrator', 'Adops Team'])
def deleteOpening(request, openingID):
    try:
        Openings.object.get(id = openingID).delete()
        messages.success(request, "Opening deleted")
    except Exception:
        messages.error(request, "Failed to delete the opening!")
    return redirect('add_openings')

def openings(request):
    try:
        academy = Academy.objects.all()[0]
    except Exception as e:
        academy = None
    openings = Openings.objects.all().order_by('-created_at')
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
        'openings': openings
    }
    return render(request, 'adops/openings/apply_opening.html', context)

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
    isinputDateValid = False
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
    return [success_msg, error_msg, isinputDateValid]

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
                    user.save()
                    UserProfile.objects.create(
                        user = user, name_prefix = nameprefix, date_of_birth = dob, gender = gender, phone = phone,
                        door_no = doorno, zip_code = zipcode, city = city, district = district, state = state, country = country,
                        photo = photo, resume = resume)
                    about_receiveing_email = "If you didn't recieve any email, please check your spam folder \
                                                            or change your internet connection"
                    try:
                        current_user = User.objects.get(username = user.username)
                        try:
                            url = 'http://127.0.0.1:4000/getEncryptionData/{}/?format=json'.format(username)
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
                    url = 'http://127.0.0.1:4000/getEncryptionData/{}/?format=json'.format(username)
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
            url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(uid)
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
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        return HttpResponse(status = 404)

@allowed_users(allowed_roles=['Applicant'])
def userAppliedOpenings(request):
    currentUser = request.user
    appliedOpenings = Openings.objects.filter(applied = currentUser)
    context = {
        'appliedOpenings':appliedOpenings,
    }
    return render(request, 'adops/openings/openingsAppliedInfo.html', context)

@allowed_users(allowed_roles=['Applicant'])
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
    
@allowed_users(allowed_roles=['Administrator', 'Adops Team'])
def applicantsInfo(request, openingID):
    if Openings.objects.filter(id = openingID, applied__isnull=False).exists() is True:
        openingApplicants = Openings.objects.get(id = openingID)
        applicants = openingApplicants.applied.all()
        for eachApplicant in applicants:
            userID = eachApplicant.id
            if User.objects.filter(id = userID).exists() is True:
                userObj = User.objects.get(id = userID)
                if UserProfile.objects.filter(user = userObj).exists() is True:
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
            staff = UserProfile.objects.get(user = userObj)
        except UserProfile.DoesNotExist:
            staff = None
        if request.method == "POST":
            skills_list = request.POST.get('skills')
            photo = request.FILES.get('photo') or None
            about = request.POST.get('about').strip()
            if about == '':
                about = None
            skills_list = skills_list.split(',')
            staff.about = about
            if photo:
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

def createProgramme(request):
    branches = Branch.objects.all()
    if request.method == "POST":
        degree = request.POST.get('degree')
        name = request.POST.get('programme')
        description = request.POST.get('prog_desc')
        duration = request.POST.get('prog_duration')
        branch_id = request.POST.get('branch_id')

        if Branch.objects.filter(id = branch_id).exists() is True:
            branchObj = Branch.objects.get(id = branch_id)
            if Programme.objects.filter(name = name).exists() is False:
                try:
                    Programme.objects.create(degree = degree, name = name, duration = duration, branch = branchObj)
                    messages.success(request, "Programme created successfully!")
                    return redirect('manageAdmission')
                except Exception as e:
                    print(e)
                    messages.error(request, e)
                    return redirect('createProgramme')
            else:
                messages.error(request, "Programme already exists!")
                return redirect('createProgramme')
        else:
            messages.error(request, "Branch doesn't exist!")
            return redirect('createProgramme')
    context = {
        "branches": branches
    }
    return render(request, 'adops/admissions/programme/createProgramme.html', context)

def editProgramme(request, programmeID):
    branches = Branch.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        branch_id = request.POST.get('branch_id')
        specialization_id = request.POST.get('specialization_id')

        if Branch.objects.filter(id = branch_id).exists() is True:
            branchObj = Branch.objects.get(id = branch_id)
            if Programme.objects.filter(id = programmeID).exists() is True:
                try:
                    updateProgramme = Programme.objects.get(id = programmeID)
                    updateProgramme.name = name
                    updateProgramme.duration = duration
                    updateProgramme.branch = branchObj
                    updateProgramme.save()
                    messages.info(request, "Programme updated successfully!")
                    return redirect('createProgramme')
                except Exception as e:
                    messages.error(request, e)
                    return redirect('editProgramme', programmeID = programmeID)
            else:
                messages.error(request, "Programme doesn't exists!")
                return redirect('manage_adops')
        else:
            messages.error(request, "Branch doesn't exist!")
            return redirect('editProgramme', programmeID = programmeID)
    context = {
        "branches": branches
    }
    return render(request, 'adops/admission/programme/editProgramme.html', context)

def deleteProgramme(request, programmeID):
    try:
        Programme.objects.get(id = programmeID).delete()
        messages.info(request, "Programme deleted successfully!")
    except Exception as e:
        messages.error(request, e)
    return redirect('manage_adops')

def manageProgrammes(request):
    programmes = Programme.objects.all()
    branches = Branch.objects.all()
    context = {
        "branches": branches,
        "specializations": specializations,
        "programmes": programmes,
    }
    return render(request, 'adops/admissions/programme/manageProgrammes.html', context)

def viewProgrammes(request):
    admissions = Admission.objects.all()
    context = {
        "admissions": admissions,
    }
    return render(request, 'adops/admissions/programme/viewProgrammes.html', context)

def manageAdmission(request):
    admissions = Admission.objects.all()
    programmes = Programme.objects.all()
    context = {
        "programmes": programmes,
        "admissions": admissions,
    }
    return render(request, 'adops/admissions/manageAdmission.html', context)

def createAdmission(request):
    if request.method == "POST":
        batchStartYear = request.POST.get('batchStartYear')
        batchEndYear = request.POST.get('batchEndYear')
        programme_id = request.POST.get('programme_id')
        admissionStatus = request.POST.get('admissionStatus')
        if admissionStatus == 'on':
            admissionStatus = True
        else:
            admissionStatus = False
        if Programme.objects.filter(id = programme_id).exists() is True:
            programmeObj = Programme.objects.get(id = programme_id)
            if Admission.objects.filter(batch_start_year = batchStartYear, batch_end_year = batchEndYear, programme = programmeObj).exists() is False:
                try:
                    Admission.objects.create(
                        batch_start_year = batchStartYear,
                        batch_end_year = batchEndYear,
                        programme = programmeObj,
                        is_active = admissionStatus
                    )
                    messages.success(request, "Admission created successfully!")
                except Exception as e:
                    messages.error(request, e)
            else:
                messages.error(request, "Admission already exists!")
            return redirect('manageAdmission')
        else:
            messages.error(request, "Programme doesn't exists!")
            return redirect('manageAdmission')
    else:
        messages.warning(request, "Can't process request!")
        return redirect('manageAdmission')

def stuAdmRegistration(request):
    gender_list = GENDERCHOICESForm()
    programmes = Programme.objects.all()
    if request.method == 'POST':
        firstname = request.POST.get('firstname').title()
        lastname = request.POST.get('lastname').title()
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email').lower()
        phone = request.POST.get('phone')
        dob = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        doorno = request.POST.get('door_no')
        zipcode = request.POST.get('zip_code')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        photo = request.FILES.get('photo') or None
        programmeID = request.POST.get('programme_id')

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            fingerprintID = request.COOKIES['U53R_876_10']
        except Exception:
            fingerprintID = None

        validatedUserDOB = validateUserDOB(dob)

        if Programme.objects.filter(id = programmeID).exists() is True:
            programmeObj = Programme.objects.get(id = programmeID)
            batchAdmObj = Admission.objects.get(programme = programmeObj, is_active = True)
            if validatedUserDOB[2] is True:
                if User.objects.filter(username=username).exists() is False:
                    if password == confirm_password:
                        try:
                            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                            admstudent, isCreated = Group.objects.get_or_create(name ='Admission Student')
                            user.groups.add(Group.objects.get(name = str(admstudent)))
                            user.is_active = False
                            user.save()
                            UserProfile.objects.create(
                                user = user, date_of_birth = dob, gender = gender, phone = phone,
                                door_no = doorno, zip_code = zipcode, city = city, district = district, state = state, country = country,
                                photo = photo)
                            AdmissionRegister.objects.create(student = user, batch = batchAdmObj)
                            StuAdmAccountVerificationStatus.objects.create(user=user, verificationStatus = False, ipaddress = ip, bfpID = fingerprintID)
                        except Exception as e1:
                            messages.error(request, str(e1))
                            try:
                                user = User.objects.get(username = username)
                                AdmissionRegister.objects.get(student = user).delete()
                                UserProfile.objects.get(user = user).delete()
                                user.delete()
                            except Exception as e2:
                                messages.error(request, str(e2))
                            return redirect('stuAdmRegistration')
                        try:
                            url = 'http://127.0.0.1:4000/getEncryptionData/{}/?format=json'.format(username)
                            response = requests.get(url)
                            dataUsername = response.json()
                        except Exception:
                            messages.info(request, "Server under maintenance. Please try again later.")
                            return redirect('stuAdmRegistration')
                        return redirect('send_stuAdm_reg_email', EnUsername = dataUsername['EncryptedUsername'])
                    else:
                        messages.info(request, "Password Didn't Match")
                        return redirect('stuAdmRegistration')
                else:
                    messages.error(request, "Username Already Exists...!")
                    return redirect('stuAdmRegistration')
            elif "not in YYYY-MM-DD format" in validatedUserDOB[1] :
                messages.error(request, str(validatedUserDOB[1]))
                return redirect('stuAdmRegistration')
        else:
            messages.error(request, "Programme Doesn't Exist")
            return redirect('stuAdmRegistration')
    context = {
        'gender': gender_list,
        'programmes': programmes,
    }
    return render(request, 'adops/admissions/apply_admission.html', context)

def send_stuAdm_reg_email(request, EnUsername):
    try:
        url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('stuAdmRegistration')
    
    isMailSent = False
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except Exception as e:
        messages.error(request, str(e))
        return redirect('stuAdmRegistration')

    if User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = False, is_staff = False, is_superuser = False).exists() is True:        
        ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=10)
        if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your admission - AkirA", created_at__gte=ten_minutes_ago).exists() is False:
            try:
                current_site = get_current_site(request)
                protocol = request.is_secure() and "https" or "http"
                mail_subject = "Confirm your admission - AkirA"
                message = render_to_string('adops/admissions/verify_stuAdm_email.html', {
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
                return redirect("waitingStuAdmConfirmation", EnUsername = EnUsername)
            except Exception as e1:
                isMailSent = False
                messages.error(request, str(e1))
                return redirect("waitingStuAdmConfirmation", EnUsername = EnUsername)
        else:
            messages.error(request, "You can't request confirm email within 10 minutes")
            return redirect("waitingStuAdmConfirmation", EnUsername = EnUsername)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def waitingStuAdmConfirmation(request, EnUsername):
    try:
        url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('stuAdmRegistration')
    ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=1000)
    last_mail_time = ''
    if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your admission - AkirA", created_at__gte=ten_minutes_ago).exists() is True:
        getlast_mail_time = MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your admission - AkirA", created_at__gte=ten_minutes_ago)
        lastObject = getlast_mail_time.last()
        last_mail_time = lastObject.created_at
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return redirect('stuAdmRegistration')
    if user.is_active is False:
        context = {
            'EnUsername': EnUsername,
            'last_mail_time': last_mail_time,
        }
        return render(request, 'adops/admissions/waitingStuAdmConfirmation.html', context)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def confirm_admission_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        try:
            url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(uid)
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
        user.save()
        getSASVS = StuAdmAccountVerificationStatus.objects.get(user__username = dataUsername['DecryptedUsername'])
        getSASVS.verificationStatus = True
        getSASVS.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        return HttpResponse(status = 404)

def isStuAdmRegConfirmed(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            fingerprintID = request.COOKIES['U53R_876_10']
        except Exception:
            fingerprintID = None
        EnUsername = request.POST.get('EnUsername')
        try:
            url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(EnUsername)
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
        isStuAdmAccountCreated = User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = True).exists()
        if isStuAdmAccountCreated is True:
            print("Here0")
            try:
                getAAVIPAddr = StuAdmAccountVerificationStatus.objects.get(user__username = dataUsername['DecryptedUsername'], verificationStatus = True)
                print("Here1")
            except Exception:
                getAAVIPAddr = None
                print("Here2")
            if str(ip) == str(getAAVIPAddr.ipaddress) or str(fingerprintID) == str(getAAVIPAddr.bfpID):
                print("Here3")
                dataResponse = {
                    'status': 'success',
                }
                print("Here4")
            print("Here5")
        print("Here6")
        print(dataResponse)
        return JsonResponse(dataResponse)

def AdmissionbyBatch(request, batchID):
    if Admission.objects.filter(id = batchID).exists() is True:
        admissionbyBatchObjs = AdmissionRegister.objects.filter(batch__id = batchID)
        context = {
            'admissionbyBatchObjs': admissionbyBatchObjs,
        }
        return render(request, 'adops/admissions/admissionbyBatch.html', context)
    else:
        messages.error(request, "Batch doesn't exist")
        return redirect('manageAdmission')

def acceptAdmissionAjax(request):
    if request.method == 'POST':
        studentID = request.POST.get('student_id')
        if User.objects.filter(username = studentID).exists() is True:
            getStudent = User.objects.get(username = studentID)
            if getStudent.groups.filter(name = 'Admission Student').exists() is True:
                studentGroup, created = Group.objects.get_or_create(name='Student')
                studentGroup.user_set.add(getStudent)
                admStudentGroup, created = Group.objects.get_or_create(name='Admission Student')
                admStudentGroup.user_set.remove(getStudent)
                message = "Student admission accepted successfully"
                status = "success"
            elif getStudent.groups.filter(name = 'Student').exists() is True:
                message = "Student Admission is already accepted"
                status = 'info'
            else:
                message = "Can't accept admission."
                status = 'error'
            return JsonResponse({'status': status, 'message': message})
        else:
            message = "Student doesn't exist"
            status = "error"
            return JsonResponse({'message': message, 'status': status})

def admstudent_dashboard(request):
    context = {

    }
    return render(request, 'adops/admissions/admstudent_dashboard.html', context)