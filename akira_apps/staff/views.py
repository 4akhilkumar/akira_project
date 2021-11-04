import io
from os import error
from django.contrib.auth import authenticate
from django.http import request
from django.http.response import HttpResponse
import pandas as pd

from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from akira_apps.academic_registration.forms import BranchForm
from akira_apps.super_admin.decorators import allowed_users
from akira_apps.authentication.forms import CreateUserForm
from akira_apps.academic_registration.models import Course, SectionRooms, Semester, course_registration_staff
from akira_apps.staff.models import Staffs
from akira_apps.student.forms import StudentsForm
from akira_apps.student.models import Students, course_registration_student

import secrets

@allowed_users(allowed_roles=['Staff'])
def staff_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/faculty_dashboard.html', context)

@allowed_users(allowed_roles=['Course Co-Ordinator'])
def cc_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/cc_dashboard.html', context)

@allowed_users(allowed_roles=['Head of the Department'])
def hod_dashboard(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'staff/hod_templates/hod_dashboard.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_courses(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    if Semester.objects.all().count() == 0:
        return redirect('create_semester')
    elif Staffs.objects.all().count() == 0:
        return redirect('add_staff')

    course_coordinator_list = User.objects.filter(groups__name='Course Co-Ordinator')
    branch_list = BranchForm()
    semester_list = Semester.objects.all()

    context = {
        "rAnd0m123":rAnd0m123,
        "course_coordinator_list":course_coordinator_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
    }
    return render(request, 'staff/hod_templates/courses_templates/create_courses.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def save_created_course(request):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code').strip()
        courseName = request.POST.get('course_name').strip()
        courseShortInfo = request.POST.get('course_short_info').strip()
        courseWywl = request.POST.get('course_wywl').strip()
        courseSywg = request.POST.get('course_sywg').strip()
        courseDesc = request.POST['course_desc']
        courseCoOrdinator = request.POST.get('course_coordinator')
        courseCoOrdinator_id = User.objects.get(id=courseCoOrdinator)
        branch_name = request.POST.get('branch')
        semester_info = request.POST.get('semester')
        semester_id = Semester.objects.get(id=semester_info)

        try:
            course = Course(course_code=courseCode, 
                            course_name=courseName, 
                            course_short_info=courseShortInfo, 
                            course_wywl=courseWywl, 
                            course_sywg=courseSywg, 
                            course_desc=courseDesc, 
                            course_coordinator=courseCoOrdinator_id,
                            branch=branch_name, 
                            semester=semester_id)
            course.save()
            return redirect('manage_courses')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def edit_course(request, course_id):
    rAnd0m123 = secrets.token_urlsafe(16)
    course = Course.objects.get(id=course_id)
    course_coordinator_list = User.objects.filter(groups__name='Course Co-Ordinator')
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    context = {
        "rAnd0m123":rAnd0m123,
        "course":course,
        "course_coordinator_list":course_coordinator_list,
        "branch_list":branch_list,
        "semester_list":semester_list
    }
    return render(request, 'staff/hod_templates/courses_templates/edit_course.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def save_edit_course(request, course_id):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code').strip()
        courseName = request.POST.get('course_name').strip()
        courseShortInfo = request.POST.get('course_short_info').strip()
        courseWywl = request.POST.get('course_wywl').strip()
        courseSywg = request.POST.get('course_sywg').strip()
        courseDesc = request.POST['course_desc']
        courseCoOrdinator = request.POST.get('course_coordinator')
        courseCoOrdinator_id = User.objects.get(id=courseCoOrdinator)
        branch_name = request.POST.get('branch')
        semester_info = request.POST.get('semester')
        semester_id = Semester.objects.get(id=semester_info)

        try:
            course = Course.objects.get(id=course_id)
            course.course_code=courseCode
            course.course_name=courseName
            course.course_short_info=courseShortInfo
            course.course_wywl=courseWywl
            course.course_sywg=courseSywg
            course.course_desc=courseDesc
            course.course_coordinator=courseCoOrdinator_id
            course.branch=branch_name
            course.semester=semester_id
            course.save()
            return redirect('manage_courses')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_courses(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('manage_courses')

def manage_courses(request):
    rAnd0m123 = secrets.token_urlsafe(16)
    list_courses = Course.objects.all()
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all()))

    staff_enrolled_course = course_registration_staff.objects.filter(staff = request.user.id)
    course_id_list = []
    for i in staff_enrolled_course:
        course_object = course_registration_staff.objects.get(id=i.id, staff=request.user.id)
        course_id = course_registration_staff.objects.get(id=course_object.id)
        course_id_list.append(str(course_id.course.id))
    course_id_list_str = ", ".join(course_id_list)

    context = {
        "rAnd0m123":rAnd0m123,
        "list_courses":list_courses,
        "group_list":group_list,
        "course_id_list_str":course_id_list_str,
    }
    return render(request, 'staff/hod_templates/courses_templates/manage_courses.html', context)

def view_course(request, course_id):
    rAnd0m123 = secrets.token_urlsafe(16)
    course = Course.objects.get(id=course_id)
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

def bulk_upload_students_save(request):
    if request.method == 'POST':
        student_from_db = User.objects.all()
        student_user=[]
        for i in student_from_db:
            student_user.append(i.username)
            student_user.append(i.email)

        paramFile = io.TextIOWrapper(request.FILES['studentfile'].file)
        data = pd.read_csv(paramFile)
        data.drop_duplicates(subset ="Username", keep = 'first', inplace = True)

        for index, row in data.iterrows():
            if str(row['Username']) not in student_user and str(row['Email']) not in student_user:
                newuser = User.objects.create_user(
                    username=row['Username'],
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    email=row['Email'],
                    password=row['Password'],
                )
                Student=Group.objects.get(name='Student')
                if row['Group'] == 'Student':
                    Student.user_set.add(newuser)
                    newuser.groups.add(Student)

                student = Students.objects.bulk_create([
                    Students(
                        user_id = newuser.id,
                        gender=row['Gender'],
                        father_name=row['Father Name'],
                        father_occ=row['Father Occupation'],
                        father_phone=row['Father Phone'],
                        mother_name=row['Mother Name'],
                        mother_tounge=row['Mother Tounge'],
                        dob=(row['Date of Birth'] if row['Date of Birth'] != '' else '1998-12-01'),
                        blood_group=row['Blood Group'],
                        phone=row['Phone'],
                        dno_sn=row['Door No.'],
                        zip_code=row['Zip Code'],
                        city_name=row['City Name'],
                        state_name=row['State Name'],
                        country_name=row['Country'],
                        branch=row['Branch']
                    )
                ])
        success_message = "Student Record(s) Imported Successfully."
        context = {
            "success_message":success_message
        }
        return redirect('manage_student', context)
    else:
        error_message = "Failed to Import Bulk Records!."
        context = {
            "error_message":error_message
        }
        return redirect('manage_student', context)

def staff_enroll_course(request, course_id):
    current_staff = User.objects.get(id=request.user.id)
    courseId = Course.objects.get(id=course_id)
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
    courseId = Course.objects.get(id=course_id)
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

# lst = course_registration_staff.objects.all()
# for i in lst:
#     unenrollCourse = course_registration_staff.objects.get(id=i.id)
#     unenrollCourse.delete()

# lst = course_registration_student.objects.all()
# for i in lst:
#     unenrollCourse = course_registration_student.objects.get(id=i.id)
#     unenrollCourse.delete()