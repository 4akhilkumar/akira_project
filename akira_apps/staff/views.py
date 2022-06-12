from email import message
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from akira_apps.adops.models import UserProfile
from akira_apps.staff.models import Designation, UserDesignation

from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.course.models import (CourseMC)
from akira_apps.academic.models import (Branch)
from akira_apps.super_admin.forms import (BLOODGROUPForm)

import secrets
import pandas as pd
import io
import csv
import datetime as pydt

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

def add_staff(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        groupName = request.POST.get('group')
        user = User.objects.create_user(
            username = username, email = email,
            password = password,
            first_name = firstname,
            last_name = lastname
        )
        user.is_active = True # False
        applicant_group, isCreated = Group.objects.get_or_create(name = groupName)
        user.groups.add(Group.objects.get(name = str(applicant_group)))
        # Staff.objects.create(user = user)
        user.save()
    context = {
    }
    return render(request, 'staff/add_staff.html', context)

def editStaff(request, username):
    staff = UserProfile.objects.get(user__username=username)
    list_groups = Group.objects.all()
    if request.method == 'POST':
        pass
    else:
        pass
    context = {
        'list_groups':list_groups,
    }
    return render(request, 'staff/staff_templates/manage_staff/edit_faculty.html', context)

def viewStaff(request, username):
    try:
        staff = User.objects.get(username=username)
    except Exception:
        messages.error(request, "Staff doesn't exist")
        return redirect('manageOpenings')
    user = User.objects.get(username=username)
    list_groups = Group.objects.all()
    current_user_group = ', '.join(map(str, user.groups.all()))
    context = {
        "staff": staff,
        "current_user_group": current_user_group,
        "list_groups": list_groups,
    }
    return render(request, "staff/viewStaff.html", context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
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

@csrf_exempt
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