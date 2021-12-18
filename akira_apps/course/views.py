from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from akira_apps.super_admin.decorators import allowed_users
from akira_apps.academic.models import (Semester)
from akira_apps.academic.forms import (BranchForm)
from akira_apps.staff.models import (Staff)
from akira_apps.authentication.models import (User_IP_B_List)
from akira_apps.course.models import (Course, CourseFiles)

def manage_courses(request):
    courses = Course.objects.all()
    context = {
        "courses":courses,
    }
    return render(request, 'course/manage_courses.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_course(request):
    if Semester.objects.all().count() == 0:
        messages.info(request, 'Please create a semester first')
        return redirect('manage_academic')
    elif Staff.objects.all().count() == 0:
        messages.info(request, 'Please create a staff first')
        return redirect('add_staff')

    faculty_list = User.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()

    context = {
        "faculty_list":faculty_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
    }
    return render(request, 'course/create_course.html', context)

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
        courseSemester = Semester.objects.get(id=courseSemester)
        courseFiles = request.FILES.getlist('course_files')
        try:

            courseObj = Course(
                course_code=courseCode,
                course_name=courseName,
                course_short_info=courseShortInfo,
                course_wywl=courseWYWL,
                course_sywg=courseSYWG,
                course_desc=courseDesc,
                course_coordinator=courseCC,
                branch=courseBranch,
                semester=courseSemester)
            courseObj.save()
            getCourseObj = Course.objects.get(course_code = courseCode)
            try:
                for file in courseFiles:
                    CourseFiles.objects.create(course = getCourseObj, course_files = file)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
        return redirect('manage_courses')

def view_course(request, course_code):
    courseObj = Course.objects.get(course_code=course_code)
    courseFilesObjs = CourseFiles.objects.filter(course = courseObj)
    context = {
        "course":courseObj,
        "courseFilesObjs":courseFilesObjs,
    }
    return render(request, 'course/view_course.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('manage_courses')

# Course.objects.all().delete()