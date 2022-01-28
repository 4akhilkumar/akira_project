from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse

from datetime import datetime

from akira_apps.super_admin.decorators import allowed_users
from akira_apps.academic.models import (Semester)
from akira_apps.academic.forms import (BranchForm)
from akira_apps.course.models import (CourseComponent, CourseExtraFields, CourseMC, CourseOfferingType, CourseFiles, CourseSubComponent, CourseTask, TaskAnswer)
from akira_apps.specialization.models import (SpecializationsMC)

@login_required(login_url=settings.LOGIN_URL)
def manage_courses(request):
    courses = CourseMC.objects.all()
    specializations = SpecializationsMC.objects.all()
    context = {
        "courses":courses,
        "specializations":specializations,
    }
    return render(request, 'course/manage_courses.html', context)

def first_letter_word(value):
    lst = value.split(" ")
    chindex=1
    arr = []
    if "and" in lst:
        lst.remove("and")
    for letter in lst:
        if chindex==1:
            arr.append(letter[0].upper().strip("&"))
        else:
            arr.append(letter)
    out = "".join(arr)
    return out

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_course(request):
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    faculty_list = User.objects.all()
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseCC = request.POST.get('course_coordinator')
        courseDesc = request.POST.get('course_desc')
        courseCC = User.objects.get(id=courseCC)
        courseBranch = request.POST.get('branch')
        courseSemester = request.POST.get('semester')
        courseSpecialization_id = request.POST.get('specialization')
        courseSpecializationObj = SpecializationsMC.objects.get(id=courseSpecialization_id)
        courseSemester = Semester.objects.get(id=courseSemester)
        courseFiles = request.FILES.getlist('course_files')
        try:
            CourseMC.objects.create(
                code=courseCode,
                name=courseName,
                short_name=first_letter_word(courseName),
                desc = courseDesc,
                course_coordinator=courseCC,
                branch=courseBranch,
                semester=courseSemester,
                specialization=courseSpecializationObj,
                )
            getCourseObj = CourseMC.objects.get(code = courseCode)
            try:
                for file in courseFiles:
                    CourseFiles.objects.create(course = getCourseObj, course_files = file)
                messages.success(request, "Course created successfully")
            except Exception as e:
                messages.error(request, e)
            try:
                pass
            except Exception:
                pass
        except Exception as e:
            messages.error(request, e)
    context = {
        "branch_list":branch_list,
        "semester_list":semester_list,
        "faculty_list":faculty_list,
    }
    return render(request, 'course/create_course.html', context)

@login_required(login_url=settings.LOGIN_URL)
def courseExtraFieldsCreate(request, courseID):
    if request.method == "POST":
        if CourseMC.objects.filter(id = courseID).exists() is True:
            getCourseObj = CourseMC.objects.get(id=courseID)
            course_field = request.POST.get('course_field')
            course_value = request.POST.get('course_value')
            try:
                CourseExtraFields.objects.create(
                    course = getCourseObj,
                    field_name = course_field,
                    field_value = course_value
                )
            except Exception as e:
                messages.info(request, e)
            return redirect('view_course', course_code = getCourseObj.course_code)
        else:
            messages.info(request, "Course does not exist")
            return redirect('manage_courses')
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def courseExtraFieldsEdit(request, courseEFVID):
    if request.method == "POST":
        if CourseExtraFields.objects.filter(id = courseEFVID).exists() is True:
            course_field = request.POST.get('course_field')
            course_value = request.POST.get('course_value')
            getCEFObj = CourseExtraFields.objects.get(id = courseEFVID)
            getCEFObj.field_name = course_field
            getCEFObj.field_value = course_value
            getCEFObj.save()
            return redirect('view_course', course_code = getCEFObj.course.code)
        else:
            messages.info(request, "EF does not exist")
            return redirect('manage_courses')
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def courseExtraFieldsDelete(request, courseEFVID):
    getCEFObj = CourseExtraFields.objects.get(id = courseEFVID)
    getCEFObj.delete()
    messages.info(request, "Exrtra field deleted successfully")
    return redirect('view_course', course_code = getCEFObj.course.code)

@login_required(login_url=settings.LOGIN_URL)
def courseOfferingCreate(request, courseID):
    if CourseMC.objects.filter(id = courseID).exists() is True:
        getCourseObj = CourseMC.objects.get(id=courseID)
        if request.method == "POST":
            name = request.POST.get('name')
            ltps = request.POST.get('ltps')
            l,t,p,s = ltps.split("-")
            CourseOfferingType.objects.create(
                course = getCourseObj,
                name = name,
                l = l,
                t = t,
                p = p,
                s = s
            )
            return redirect('view_course', course_code = getCourseObj.code)
        else:
            messages.info(request, "We could process your request!")
            return redirect('view_course', course_code = getCourseObj.code)
    else:
        messages.info(request, "Course does not exist")
        return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def courseOfferingEdit(request, cOTID):
    if CourseOfferingType.objects.filter(id = cOTID).exists() is True:
        getCoursOTeObj = CourseOfferingType.objects.get(id=cOTID)
        if request.method == "POST":
            name = request.POST.get('name')
            ltps = request.POST.get('ltps')
            l,t,p,s = ltps.split("-")
            getCoursOTeObj.name = name
            getCoursOTeObj.l = l,
            getCoursOTeObj.t = t,
            getCoursOTeObj.p = p,
            getCoursOTeObj.s = s
            getCoursOTeObj.save()
            return redirect('view_course', course_code = getCoursOTeObj.course.code)
        else:
            messages.info(request, "We could process your request!")
            return redirect('view_course', course_code = getCoursOTeObj.course.code)
    else:
        messages.info(request, "COT does not exist")
        return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def courseOfferingDelete(request, CourseOfferingID):
    try:
        getCOTbj = CourseOfferingType.objects.get(id = CourseOfferingID)
        getCOTbj.delete()
        messages.info(request, "Course Offering deleted successfully")
    except Exception:
        messages.info(request, "Course Offering does not exist")
    return redirect('manage_courses')

@login_required(login_url=settings.LOGIN_URL)
def view_course(request, course_code):
    try:
        courseObj = CourseMC.objects.get(course_code=course_code)
        courseFilesObjs = CourseFiles.objects.filter(course = courseObj)
    except Exception:
        messages.info(request, "No such course exist")
        return redirect('manage_courses')
    faculty_list = User.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    try:
        courseComponent = CourseComponent.objects.filter(course = courseObj)
        courseSubComponent = CourseSubComponent.objects.filter(course = courseObj)
        courseTask = CourseTask.objects.filter(course = courseObj)
        taskAnswer = TaskAnswer.objects.filter(course = courseObj, user = request.user)
    except Exception:
        courseComponent = None
        courseSubComponent = None
        courseTask = None
        taskAnswer = None
    context = {
        "course":courseObj,
        "courseFilesObjs":courseFilesObjs,
        "faculty_list":faculty_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
        "courseComponent":courseComponent,
        "courseSubComponent":courseSubComponent,
        "courseTask":courseTask,
        "taskAnswer":taskAnswer,
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

def course_component(request):
    if request.method == "POST":
        courseId = request.POST.get('course')
        component = request.POST.get('component')
        desc = request.POST.get('desc')
        try:
            getCourseObj = CourseMC.objects.get(id=courseId)
            CourseComponent.objects.create(course = getCourseObj,
                                            name = component,
                                            desc = desc)
            return redirect('view_course', course_code = getCourseObj.course_code)
        except Exception:
            messages.info(request, "Failed to create component")
            return redirect('view_course', course_code = getCourseObj.course_code)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

def sub_component(request):
    if request.method == "POST":
        courseId = request.POST.get('course')
        componentId = request.POST.get('component')
        subComponent = request.POST.get('sub_component')
        desc = request.POST.get('desc')
        try:
            getCourseObj = CourseMC.objects.get(id=courseId)
            getComponentObj = CourseComponent.objects.get(id=componentId)
            CourseSubComponent.objects.create(course = getCourseObj,
                                            component = getComponentObj,
                                            name = subComponent,
                                            desc = desc)
            return redirect('view_course', course_code = getCourseObj.course_code)
        except Exception:
            messages.info(request, "Failed to create sub component")
            return redirect('view_course', course_code = getCourseObj.course_code)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')
    
def course_task(request):
    if request.method == "POST":
        courseId = request.POST.get('course')
        componentId = request.POST.get('component-course-task')
        subComponentId = request.POST.get('subcomponent')
        question = request.POST.get('question')
        try:
            getCourseObj = CourseMC.objects.get(id=courseId)
            getComponentObj = CourseComponent.objects.get(id=componentId)
            getSubComponentObj = CourseSubComponent.objects.get(id=subComponentId)
            CourseTask.objects.create(course = getCourseObj,
                                            component = getComponentObj,
                                            sub_component = getSubComponentObj,
                                            question = question)
            return redirect('view_course', course_code = getCourseObj.course_code)
        except Exception as e:
            print(e)
            messages.info(request, "Failed to create course Task")
            return redirect('view_course', course_code = getCourseObj.course_code)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

def task_answer(request):
    if request.method == "POST":
        courseId = request.POST.get('course')
        componentId = request.POST.get('component')
        subComponentId = request.POST.get('subcomponent')
        questionId = request.POST.get('task')
        answer = request.FILES.get('answer')
        try:
            getCourseObj = CourseMC.objects.get(id=courseId)
            getComponentObj = CourseComponent.objects.get(id=componentId)
            getSubComponentObj = CourseSubComponent.objects.get(id=subComponentId)
            getTaskObj = CourseTask.objects.get(id=questionId)
            TaskAnswer.objects.create(user = request.user,
                                        course = getCourseObj,
                                        component = getComponentObj,
                                        sub_component = getSubComponentObj,
                                        task = getTaskObj,
                                        answer = answer)
            return redirect('submitSolutionPage', task_id = questionId)
        except Exception as e:
            print(e)
            messages.info(request, "Failed to submit answer")
            return redirect('view_course', task_id = questionId)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_courses')

def submitSolutionPage(request, task_id):
    getTaskObj = CourseTask.objects.get(id=task_id)
    taskCourse = getTaskObj.course
    taskComponent = getTaskObj.component
    taskSubComponent = getTaskObj.sub_component
    taskAnswer = TaskAnswer.objects.filter(task = getTaskObj, user = request.user)
    context = {
        "taskCourse":taskCourse,
        "taskComponent":taskComponent,
        "taskSubComponent":taskSubComponent,
        "getTaskObj":getTaskObj,
        "taskAnswer":taskAnswer,
    }
    return render(request, 'course/submitSolution.html', context)

def subComponentsbyComponents(request):
    if request.method == "POST":
        component_id = request.POST['component']
        try:
            getSubComponents = CourseSubComponent.objects.filter(component__id=component_id)
        except Exception as e:
            print(e)
        return JsonResponse(list(getSubComponents.values('id', 'name')), safe = False) 