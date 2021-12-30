from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from datetime import datetime

from akira_apps.super_admin.decorators import allowed_users
from akira_apps.academic.models import (Semester)
from akira_apps.academic.forms import (BranchForm)
from akira_apps.course.models import (CourseMC, CourseFiles)
from akira_apps.specialization.models import (SpecializationsMC)

@login_required(login_url=settings.LOGIN_URL)
def manage_courses(request):
    courses = CourseMC.objects.all()
    faculty_list = User.objects.all()
    specializations = SpecializationsMC.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    context = {
        "courses":courses,
        "faculty_list":faculty_list,
        "specializations":specializations,
        "branch_list":branch_list,
        "semester_list":semester_list,
    }
    return render(request, 'course/manage_courses.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_course_save(request):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseShortInfo = request.POST.get('course_short_info')
        courseWYWL = request.POST.get('course_wywl')
        courseSYWG = request.POST.get('course_sywg')
        courseDesc = request.POST.get('course_desc')
        courseCC = request.POST.get('course_coordinator')
        courseCC = User.objects.get(id=courseCC)
        courseBranch = request.POST.get('branch')
        courseSemester = request.POST.get('semester')
        courseSpecialization_id = request.POST.get('specialization')
        courseSpecializationObj = SpecializationsMC.objects.get(id=courseSpecialization_id)
        courseSemester = Semester.objects.get(id=courseSemester)
        courseFiles = request.FILES.getlist('course_files')
        try:
            CourseMC.objects.create(
                course_code=courseCode,
                course_name=courseName,
                course_short_info=courseShortInfo,
                course_wywl=courseWYWL,
                course_sywg=courseSYWG,
                course_desc=courseDesc,
                course_coordinator=courseCC,
                branch=courseBranch,
                semester=courseSemester,
                specialization=courseSpecializationObj)
            getCourseObj = CourseMC.objects.get(course_code = courseCode)
            try:
                for file in courseFiles:
                    CourseFiles.objects.create(course = getCourseObj, course_files = file)
                messages.success(request, "Course created successfully")
            except Exception as e:
                messages.error(request, e)
        except Exception as e:
            messages.error(request, e)
        return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def view_course(request, course_code):
    courseObj = CourseMC.objects.get(course_code=course_code)
    courseFilesObjs = CourseFiles.objects.filter(course = courseObj)
    faculty_list = User.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    edit_course = False
    context = {
        "course":courseObj,
        "courseFilesObjs":courseFilesObjs,
        "faculty_list":faculty_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
        "edit_course":edit_course,
    }
    return render(request, 'course/view_course.html', context)

@login_required(login_url=settings.LOGIN_URL)
def search_course(request):
    if request.method == 'POST':
        query = request.POST['search'].strip()
        beforeSearch = datetime.now()
        courses = CourseMC.objects.filter(
            Q(course_code__icontains=query) | Q(course_name__icontains=query) |
            Q(course_short_info__icontains=query) | Q(course_wywl__icontains=query) |
            Q(course_sywg__icontains=query) | Q(course_desc__icontains=query) |
            Q(course_coordinator__first_name__icontains=query) | Q(course_coordinator__last_name__icontains=query) |
            Q(branch__icontains=query) | Q(semester__mode__icontains=query) | Q(specialization__specialization_name__icontains=query) |
            Q(semester__start_year__icontains=query) | Q(semester__end_year__icontains=query)
        )
        afterSearch = datetime.now()
        totalTimeTaken = (afterSearch - beforeSearch).total_seconds()
        context = {
            'courses': courses,
            'totalTimeTaken':totalTimeTaken,
            'query':query,
        }
        return render(request, 'course/search_course.html', context)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_course(request, course_id):
    course = CourseMC.objects.get(id=course_id)
    course.delete()
    return redirect('manage_courses')