from django.contrib.auth import authenticate
from django.http.response import HttpResponse

from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.authentication.forms import (CreateUserForm)
from .models import (Staff)
from akira_apps.student.forms import (StudentsForm)
from akira_apps.course.models import (CourseMC)

import secrets
import pandas as pd
import io
import csv
import datetime as pydt

@allowed_users(allowed_roles=['Assistant Professor', 'Associate Professor', 'Professor'])
def staff_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/staff_templates/staff_dashboard.html', context)

@allowed_users(allowed_roles=['Head of the Department'])
def hod_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/hod_templates/hod_dashboard.html', context)
    
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

@allowed_users(allowed_roles=['Administrator'])
def add_student(request):
    form = CreateUserForm()
    student_form = StudentsForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        student_form = StudentsForm(request.POST,request.FILES)
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)
        username = request.POST.get('username')
        if username in student_user:
            print("A user already exist with "+ username)
            return redirect('add_student')

        if form.is_valid() and student_form.is_valid():
            user = form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username = username, password = password)

            group = Group.objects.get(name='Student')
            user.groups.add(group)
            print("Student Registered Successfully.")
            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            student_form = StudentsForm()

    context = {'form':form, 'student_form':student_form}        
    return render(request, 'staff/admission_templates/add_student.html', context)

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

def manage_staff(request):
    staffs = Staff.objects.all()
    doctorial_faculty = Staff.objects.filter(name_prefix='Dr')
    courses = CourseMC.objects.all()
    context = {
        "staffs":staffs,
        "doctorial_faculty":doctorial_faculty,
        "courses":courses,
    }
    return render(request, 'staff/staff_templates/manage_staff/manage_faculty.html', context)

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
            my_group = Group.objects.get(name='%s' % str(assigned_group)) 
            userObj = User.objects.get(username=username)
            my_group.user_set.add(userObj)
            return redirect('manage_staff')
        else:
            form = CreateUserForm()
            staff_form = StaffsForm()

    context = {
        'form':form,
        'staff_form':staff_form,
        'list_groups':list_groups,
    }       
    return render(request, 'staff/staff_templates/manage_staff/add_faculty.html', context)

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
    return render(request, 'staff/staff_templates/manage_staff/edit_faculty.html', context)

def view_staff(request, staff_username):
    staff = Staff.objects.get(user__username=staff_username)
    user = User.objects.get(username=staff_username)
    list_groups = Group.objects.all()
    current_user_group = ', '.join(map(str, user.groups.all()))
    context = {
        "staff": staff,
        "current_user_group":current_user_group,
        "list_groups":list_groups,
    }
    return render(request, "staff/staff_templates/manage_staff/view_faculty.html", context)

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