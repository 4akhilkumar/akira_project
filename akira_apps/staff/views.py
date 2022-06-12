from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from akira_apps.academic.models import (Branch)
from akira_apps.adops.models import (UserAccountVerificationStatus, UserProfile)
from akira_apps.adops.forms import (GroupTypesForm)
from akira_apps.authentication.token import (account_activation_token)
from akira_apps.course.models import (CourseMC)
from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.staff.models import (Designation, UserDesignation)
from akira_apps.super_admin.forms import (BLOODGROUPForm, GENDERCHOICESForm, NAMEPREFIXForm)
from akira_apps.super_admin.models import (MailLog)

import csv
import datetime as pydt
import io
import pandas as pd
import re
import requests
import secrets

@allowed_users(allowed_roles=['Applicant'])
def applicant_dashboard(request):
    context = {

    }
    return render(request, 'staff/dashboards/applicant_dashboard.html', context)

@allowed_users(allowed_roles=['ADOPS Team'])
def adops_dashboard(request):
    context = {

    }
    return render(request, 'staff/dashboards/adops_dashboard.html', context)

def teachingstaff_dashboard(request):
    context = {
    }
    return render(request, 'staff/dashboards/teachingstaff_dashboard.html', context)
    
def view_course(request, course_id):
    rAnd0m123 = secrets.token_urlsafe(16)
    course = CourseMC.objects.get(id=course_id)
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all())) 

    staff_enrolled_course = course_registration_staff.objects.filter(staff = request.user.id)
    course_id_list = []
    for i in staff_enrolled_course:
        course_object = course_registration_staff.objects.get(id=i.id, staff=request.user.id)
        course_id = course_registration_staff.objects.get(id=course_object.id)
        course_id_list.append(str(course_id.course.id))
    course_id_list_str = ", ".join(course_id_list)

    student_enrolled_course = course_registration_student.objects.filter(student = request.user.id)
    student_course_id_list = []
    for i in student_enrolled_course:
        course_object = course_registration_student.objects.get(id=i.id, student=request.user.id)
        course_id = course_registration_student.objects.get(id=course_object.id)
        student_course_id_list.append(str(course_id.course.id))
    student_course_id_list_str = ", ".join(student_course_id_list)

    # count_enrolled = course_registration_staff.objects.filter(course=course.id).count()

    enrolled_staff = course_registration_staff.objects.filter(course=course.id)
    staff_course_enrolled_list = []
    for i in enrolled_staff:
        staff_course_enrolled_list.append(i.staff)
    
    staff_course_enrolled_list_set = [i for n, i in enumerate(staff_course_enrolled_list) if i not in staff_course_enrolled_list[:n]]

    enrolled_students = course_registration_student.objects.filter(course=course.id)
    student_course_enrolled_list = []
    for i in enrolled_students:
        student_course_enrolled_list.append(i.student)
    
    section_list = SectionRooms.objects.all()

    course_enrolled_staff = course_registration_staff.objects.filter(course=course.id, staff=request.user.id)
    course_enrolled_section_list = []
    for i in course_enrolled_staff:
        course_enrolled_section_list.append(i.section)

    course_enrolled_section_list_str = ', '.join(map(str, course_enrolled_section_list))

    course_enrolled_student = course_registration_student.objects.filter(course=course.id, student=request.user.id)
    student_course_enrolled_section_list = []
    for i in course_enrolled_student:
        student_course_enrolled_section_list.append(i.section)

    student_course_enrolled_section_list_str = ', '.join(map(str, student_course_enrolled_section_list))

    instructor_enrolled_section_list = []
    for i in enrolled_staff:
        instructor_enrolled_section_list.append(i.section)

    # keys = []
    # values = []
    # dicts = {}
    # for i in course_enrolled_staff:
    #     keys.append(i.section)
    #     values.append(i.section.section_name)
    # for i in range(len(keys)):
    #     dicts[keys[i]] = values[i]

    context = {
        "rAnd0m123":rAnd0m123,
        "view_course":course,
        "group_list":group_list,
        "course_id_list_str":course_id_list_str,
        # "count_enrolled":count_enrolled,
        "staff_course_enrolled_list_set":staff_course_enrolled_list_set,
        "student_course_enrolled_list":student_course_enrolled_list,
        "student_course_id_list_str":student_course_id_list_str,
        "section_list":section_list,
        "course_enrolled_section_list":course_enrolled_section_list,
        "course_enrolled_section_list_str":course_enrolled_section_list_str,
        "student_course_enrolled_section_list":student_course_enrolled_section_list,
        "student_course_enrolled_section_list_str":student_course_enrolled_section_list_str,
        "instructor_enrolled_section_list":instructor_enrolled_section_list,
        # "dicts":dicts,
    }
    return render(request, 'staff/hod_templates/courses_templates/view_course.html', context)

def staff_enroll_course(request, course_id):
    current_staff = User.objects.get(id=request.user.id)
    courseId = CourseMC.objects.get(id=course_id)
    sectionRoom = request.POST.get('section')
    sectionRoom_Id = SectionRooms.objects.get(id=sectionRoom)
    try:
        enroll_course = course_registration_staff(staff = current_staff, course = courseId, section=sectionRoom_Id)
        enroll_course.save()
        return redirect('manage_courses')
    except Exception as e:
        if str(e) == "UNIQUE constraint failed: academic_registration_course_registration_staff.course_id, academic_registration_course_registration_staff.section_id":
            return HttpResponse("Your enroll for this course to this section is already done by you.")
        else:
            return HttpResponse(e)

def staff_unenroll_course(request, staff_enroll_course_id):
    try:
        unenrollCourse = course_registration_staff.objects.get(id=staff_enroll_course_id)
        unenrollCourse.delete()
        return redirect('manage_courses')
    except Exception as e:
        return HttpResponse(e)
    
def student_enroll_course(request, course_id):
    current_student = User.objects.get(id=request.user.id)
    courseId = CourseMC.objects.get(id=course_id)
    sectionRoom = request.POST.get('section')
    sectionRoom_Id = SectionRooms.objects.get(id=sectionRoom)
    try:
        enroll_course = course_registration_student(student = current_student, course = courseId, section=sectionRoom_Id)
        enroll_course.save()
        return redirect('manage_courses')
    except Exception as e:
        if str(e) == "UNIQUE constraint failed: student_course_registration_student.course_id, student_course_registration_student.section_id":
            return HttpResponse("Your enroll for this course is already done by you.")
        else:
            return HttpResponse(e)

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

def add_staff(request):
    name_prefix_list = NAMEPREFIXForm()
    gender_list = GENDERCHOICESForm()
    groups_list = GroupTypesForm()
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email').lower()
        groupName = request.POST.get('group')

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

        formResponse = dict(request.POST)
        if all(len(formResponse[key]) > 0 for key in formResponse) and not all(str(formResponse[key]).isspace() for key in formResponse):
            can_go_on = False
            if(not request.POST.get('city').isspace() or len(request.POST.get('city')) > 0) and (request.POST.get('new_city').isspace() or len(request.POST.get('new_city')) == 0):
                can_go_on = True
            elif(request.POST.get('city').isspace() or len(request.POST.get('city')) == 0) and (not request.POST.get('new_city').isspace() or len(request.POST.get('new_city')) > 0):
                can_go_on = True
            else:
                can_go_on = False
        if can_go_on is True:
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
            if validatedUserDOB[0] is True:
                try:
                    url = 'http://127.0.0.1:4000/getEmail/{}/?format=json'.format(email)
                    response = requests.get(url)
                    dataEmail = response.json()
                except Exception:
                    messages.info(request, "Server under maintenance. Please try again later.")
                    return redirect('adminInstituteRegistration')
                if dataEmail['ValidEmail'] is True and dataEmail['Disposable'] is False:
                    if not User.objects.filter(username=username).exists():
                        if password == confirm_password:
                            try:
                                user = User.objects.create_superuser(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                                staffgroup, isCreated = Group.objects.get_or_create(name = groupName)
                                user.groups.add(Group.objects.get(name = str(staffgroup)))
                                user.is_active = False
                                user.save()
                                UserProfile.objects.create(
                                    user = user, name_prefix = nameprefix, date_of_birth = dob, gender = gender, phone = phone,
                                    door_no = doorno, zip_code = zipcode, city = city, district = district, state = state, country = country,
                                    photo = photo)
                                UserAccountVerificationStatus.objects.create(user=user, verificationStatus = False, ipaddress = ip, bfpID = fingerprintID)
                                try:
                                    url = 'http://127.0.0.1:4000/getEncryptionData/{}/?format=json'.format(username)
                                    response = requests.get(url)
                                    dataUsername = response.json()
                                except Exception:
                                    messages.info(request, "Server under maintenance. Please try again later.")
                                    return redirect('add_staff')
                                return redirect('send_staff_reg_email', EnUsername = dataUsername['EncryptedUsername'])
                            except Exception:
                                if User.objects.filter(username=username).exists() is True:
                                    currentUserObj = User.objects.get(username=username)
                                    if UserAccountVerificationStatus.objects.filter(user=user).exists() is True:
                                        UserAccountVerificationStatus.objects.get(user=user).delete()
                                    if UserProfile.objects.filter(user=user).exists() is True:
                                        UserProfile.objects.get(user=user).delete()
                                    currentUserObj.delete()
                                messages.info(request, "Something went wrong. Please try again later.")
                                return redirect('add_staff')
                        else:
                            messages.info(request, "Password didn't Matched")
                            return redirect('add_staff')
                    else:
                        messages.error(request, "Username Already Exists...!")
                        return redirect('add_staff')
                elif dataEmail['Disposable'] is True:
                    messages.error(request, "Don't use disposable email address")
                    return redirect('add_staff')
                else:
                    messages.error(request, "Please use legitimate email address only")
                    return redirect('add_staff')
            elif "not in YYYY-MM-DD format" in validatedUserDOB[1] :
                messages.error(request, str(validatedUserDOB[1]))
                return redirect('add_staff')
            elif validatedUserDOB[1] == "False":
                return HttpResponse("You are not eligible to register as a Staff")
        else:
            messages.error(request, "Please fill all the fields")
            return redirect('add_staff')
    context = {
        'name_prefix': name_prefix_list,
        'gender': gender_list,
        'groups_list': groups_list,
    }
    return render(request, 'staff/add_staff.html', context)

def send_staff_reg_email(request, EnUsername):
    try:
        url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('add_staff')
    
    isMailSent = False
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except Exception as e:
        messages.error(request, str(e))
        return redirect('add_staff')

    if User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = False).exists() is True:        
        ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=10)
        if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your account registration - AkirA", created_at__gte=ten_minutes_ago).exists() is False:
            try:
                current_site = get_current_site(request)
                protocol = request.is_secure() and "https" or "http"
                mail_subject = "Confirm your account registration - AkirA"
                message = render_to_string('staff/staffVerification/verify_staff_email.html', {
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
                return redirect("waitingStaffConfirmation", EnUsername = EnUsername)
            except Exception as e1:
                isMailSent = False
                messages.error(request, str(e1))
                return redirect("waitingStaffConfirmation", EnUsername = EnUsername)
        else:
            messages.error(request, "You can't request confirm email within 10 minutes")
            return redirect("waitingStaffConfirmation", EnUsername = EnUsername)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def waitingStaffConfirmation(request, EnUsername):
    try:
        url = 'http://127.0.0.1:4000/getDecryptionData/{}/?format=json'.format(EnUsername)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('add_staff')
    ten_minutes_ago = pydt.datetime.now() - pydt.timedelta(minutes=1000)
    last_mail_time = ''
    if MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your account registration - AkirA", created_at__gte=ten_minutes_ago).exists() is True:
        getlast_mail_time = MailLog.objects.filter(user__username = dataUsername['DecryptedUsername'], subject = "Confirm your account registration - AkirA", created_at__gte=ten_minutes_ago)
        lastObject = getlast_mail_time.last()
        last_mail_time = lastObject.created_at
    try:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
    except User.DoesNotExist:
        messages.error(request, "User doesn't exist")
        return redirect('add_staff')
    if user.is_active is False:
        context = {
            'EnUsername': EnUsername,
            'last_mail_time': last_mail_time,
        }
        return render(request, 'staff/staffVerification/waitingStaffConfirmation.html', context)
    else:
        messages.info(request, "Your account registration is already confirmed")
        return redirect('login')

def confirm_staff_email(request, uidb64, token):
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
        getSASVS = UserAccountVerificationStatus.objects.get(user__username = dataUsername['DecryptedUsername'])
        getSASVS.verificationStatus = True
        getSASVS.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        return HttpResponse(status = 404)

def isStaffRegConfirmed(request):
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
        isStaffAccountCreated = User.objects.filter(username = dataUsername['DecryptedUsername'], is_active = True).exists()
        if isStaffAccountCreated is True:
            print("Here0")
            try:
                getAAVIPAddr = UserAccountVerificationStatus.objects.get(user__username = dataUsername['DecryptedUsername'], verificationStatus = True)
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

def CreateDesignationAjax(request):
    if request.method == "POST":
        designationName = request.POST.get('designation')
        designationDescription = request.POST.get('description')
        if Designation.objects.filter(name = designationName).exists() is False:
            Designation.objects.create(name = designationName, description = designationDescription)
            message = "Designation created successfully"
            status = "success"
        else:
            message = "Designation already exists!"
            status = "error"
    return JsonResponse({'message': message, 'status': status}, safe=False)

def setUserDesignationAjax(request):
    if request.method == "POST":
        userName = request.POST.get('username')
        designationName = request.POST.get('designation')
        branchID = request.POST.get('branch')
        if User.objects.filter(username = userName).exists() is True:
            userObj = User.objects.get(username = userName)
            if Branch.objects.filter(id = branchID).exists() is True:
                branchObj = Branch.objects.get(id = branchID)
                if Designation.objects.filter(name = designationName).exists() is True:
                    designationObj = Designation.objects.get(name = designationName)
                    if UserDesignation.objects.filter(user = userObj).exists() is False:
                        UserDesignation.objects.create(user = userObj, designation = designationObj, branch = branchObj)
                        message = "Designation allocated successfully"
                        status = "success"
                    elif UserDesignation.objects.filter(user = userObj, designation = designationObj).exists() is True:
                        message = "User already allocated in this designation"
                        status = "error"
                    else:
                        message = "Only one designation for each user!"
                        status = "error"
                else:
                    message = "Designation doesn't exist!"
                    status = "error"
            else:
                message = "Branch doesn't exist!"
                status = "error"
        else:
            message = "User doesn't exist!"
            status = "error"
    return JsonResponse({'message': message, 'status': status}, safe=False)

def staff_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=staff_info_record' + \
        str(pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 
                    'Name Prefix', 'Gender', 'Date of Birth',
                    'Blood Group', 'Door No.', 'Zip Code', 'City Name', 
                    'State Name', 'Country', 'Branch', 'Current Medical Issue', 'Designation'])
    
    staff = UserProfile.objects.all()

    for i in staff:
        writer.writerow([i.user.username, i.user.first_name, i.user.last_name, i.user.email,
                        i.name_prefix, i.gender, i.date_of_birth,
                        i.blood_group, i.door_no, i.zip_code, i.city_name, 
                        i.state_name, i.country_name, i.branch, i.current_medical_issue, ', '.join(map(str, i.user.groups.all()))])
    return response

def bulk_upload_staffs_save(request):
    if request.method == 'POST':
        paramFile = io.TextIOWrapper(request.FILES['staff_file'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if User.objects.filter(username = str(row['Username']).lower(), email = str(row['Email']).lower()).exists() is False:
                newuser = User.objects.create_user(
                    username=str(row['Username']).lower(),
                    first_name=str(row['First Name']).title(),
                    last_name=str(row['Last Name']).title(),
                    email=str(row['Email']).lower(),
                    password="AKIRAaccount@21",
                )
                group_name = str(row['Designation']).title()
                my_group = Group.objects.get(name='%s' % str(group_name))
                my_group.user_set.add(newuser)

                staff = UserProfile.objects.bulk_create([
                    UserProfile(
                        user_id = newuser.id,
                        name_prefix=row['Name Prefix'],
                        gender=str(row['Gender']),
                        date_of_birth=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        door_no=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city=row['City Name'],
                        district=row['District Name'],
                        state=row['State Name'],
                        country=row['Country'],
                        blood_group=row['Blood Group'],
                    )
                ])
        return redirect('manageOpenings')
    else:
        return redirect('manageOpenings')