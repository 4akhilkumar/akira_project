from email import message
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from datetime import datetime

from akira_apps.academic.forms import (SemesterModeForm)
from akira_apps.academic.models import (Semester, Branch)
from akira_apps.course.forms import (CourseTypeForm, CourseExtraFieldForm)
from akira_apps.course.models import (CourseComponent, CourseExtraFields, CourseMC, CourseOfferingType, CourseCOTExtraFields, CourseFiles, CourseSubComponent, CourseTask, TaskAnswer)
from akira_apps.specialization.models import (SpecializationsMC)
from akira_apps.super_admin.decorators import (allowed_users)

@login_required(login_url=settings.LOGIN_URL)
def manage_courses(request):
    courses = CourseMC.objects.all()
    specializations = SpecializationsMC.objects.all()
    context = {
        "courses":courses,
        "specializations":specializations,
    }
    return render(request, 'course/manage_courses.html', context)

def createCourseAjax(request):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseDesc = request.POST.get('course_desc')
        courseBranch = request.POST.get('branch')
        courseSemester = request.POST.get('semester')
        courseCC = request.POST.get('course_coordinator')
        course_type = request.POST.get('course_type')
        courseSpecialization_id = request.POST.get('specialization', None)
        pre_requisite = request.POST.get('prerequisite')
        courseFiles = request.FILES.getlist('course_files')
        
        if CourseMC.objects.filter(Q(code=courseCode) | Q(name = courseName)).exists() is False:
            if User.objects.filter(id=courseCC).exists() is True:
                courseCC = User.objects.get(id=courseCC)
                if Branch.objects.filter(id = courseBranch).exists() is True:
                    courseBranch = Branch.objects.get(id = courseBranch)
                    if Semester.objects.filter(id = courseSemester).exists() is True:
                        courseSemester = Semester.objects.get(id = courseSemester)
                        if pre_requisite == '' or pre_requisite == None or pre_requisite == 'None':
                            pre_requisite = None
                        if courseSpecialization_id is None or courseSpecialization_id == '':
                            courseSpecializationObj = None
                        else:
                            if SpecializationsMC.objects.filter(id = courseSpecialization_id).exists() is True:
                                courseSpecializationObj = SpecializationsMC.objects.get(id = courseSpecialization_id)
                        getCourseObj = CourseMC.objects.create(
                            code=courseCode,
                            name=courseName,
                            desc = courseDesc,
                            course_coordinator=courseCC,
                            branch=courseBranch,
                            semester=courseSemester,
                            specialization=courseSpecializationObj,
                            type = course_type,
                            pre_requisite = pre_requisite,
                        )
                        try:
                            for file in courseFiles:
                                CourseFiles.objects.create(course = getCourseObj, course_files = file)
                            message = "Course created successfully"
                            status = "success"
                            return JsonResponse({
                                    'message': message,
                                    'status': status,
                                    'course_id': getCourseObj.id,
                                })
                        except Exception as e:
                            message = str(e)
                            status = "error"
                    else:
                        message = "Semester does not exist"
                        status = "error"
                else:
                    message = "Branch does not exist"
                    status = "error"
            else:
                message = "User does not exist"
                status = "error"
        else:
            message = "Course with this code or name already exists"
            status = "error"
        return JsonResponse({
                'message': message,
                'status': status
            })
    else:
        message = "We could process your request!"
        status = "error"
        return JsonResponse({
                'message':message,
                'status':status
            })

def editCourse(request, course_id):

    try:
        current_courseObj = CourseMC.objects.get(code=course_id)
    except CourseMC.DoesNotExist:
        current_courseObj = None
        messages.info(request, "Course doesn't exists!")
        return redirect('manage_courses')
    courseExtraFields = CourseExtraFields.objects.filter(course = current_courseObj)

    try:
        getCreatedCourseCotCookie = request.COOKIES['course_cot_id']
    except Exception:
        getCreatedCourseCotCookie = None
    current_courseCOTObjs = None
    if getCreatedCourseCotCookie is not None:
        try:
            current_courseCOTObjs = CourseOfferingType.objects.get(id=getCreatedCourseCotCookie)
        except CourseOfferingType.DoesNotExist:
            current_courseCOTObjs = None
    current_courseCOTObjs = CourseOfferingType.objects.filter(course = current_courseObj)

    courseCOTExtraFields = CourseCOTExtraFields.objects.filter(course__course = current_courseObj)

    branch_list = Branch.objects.all()
    semester_list = Semester.objects.all()
    semesterModeForm = SemesterModeForm()
    courseTypeForm = CourseTypeForm()
    courseExtraFieldTypeForm = CourseExtraFieldForm()
    faculty_list = User.objects.all()
    specialization_list = SpecializationsMC.objects.all()
    prerequisiteList = CourseMC.objects.all()
    context = {
        "courseObj": current_courseObj,
        "courseExtraFields": courseExtraFields,
        "cots": current_courseCOTObjs,
        "courseCotExtraFields": courseCOTExtraFields,
        "branch_list":branch_list,
        "semesterModeForm":semesterModeForm,
        "semester_list":semester_list,
        "faculty_list":faculty_list,
        "courseTypeForm": courseTypeForm,
        'courseExtraFieldTypeForm':courseExtraFieldTypeForm,
        "specialization_list":specialization_list,
        "prerequisiteList": prerequisiteList,
    }
    return render(request, "course/edit_course.html", context)

def submitcourseformAjax(request):
    if request.method == 'POST':
        courseCode = request.POST.get('course_code')
        courseName = request.POST.get('course_name')
        courseDesc = request.POST.get('course_desc')
        courseBranch = request.POST.get('branch')
        courseSemester = request.POST.get('semester')
        courseCC = request.POST.get('course_coordinator')
        course_type = request.POST.get('course_type')
        courseSpecialization_id = request.POST.get('specialization', None)
        pre_requisite = request.POST.get('prerequisite')
        courseFiles = request.FILES.getlist('course_files')
        
        if CourseMC.objects.filter(code=courseCode, name = courseName).exists() is True:
            if User.objects.filter(id=courseCC).exists() is True:
                courseCCObj = User.objects.get(id=courseCC)
                if Branch.objects.filter(id = courseBranch).exists() is True:
                    courseBranch = Branch.objects.get(id = courseBranch)
                    if Semester.objects.filter(id = courseSemester).exists() is True:
                        courseSemester = Semester.objects.get(id = courseSemester)
                        if pre_requisite == '' or pre_requisite == None or pre_requisite == 'None':
                            pre_requisite = None
                        if courseSpecialization_id is None or courseSpecialization_id == '':
                            courseSpecializationObj = None
                        else:
                            if SpecializationsMC.objects.filter(id = courseSpecialization_id).exists() is True:
                                courseSpecializationObj = SpecializationsMC.objects.get(id = courseSpecialization_id)
                        getCourseObj = CourseMC.objects.get(code=courseCode)
                        getCourseObj.code=courseCode
                        getCourseObj.name=courseName
                        getCourseObj.desc = courseDesc
                        getCourseObj.course_coordinator=courseCCObj
                        getCourseObj.branch=courseBranch
                        getCourseObj.semester=courseSemester
                        getCourseObj.specialization=courseSpecializationObj
                        getCourseObj.type = course_type
                        getCourseObj.pre_requisite = pre_requisite
                        getCourseObj.save()
                        try:
                            for file in courseFiles:
                                CourseFiles.objects.create(course = getCourseObj, course_files = file)
                            message = "Course created successfully"
                            status = "success"
                        except Exception as e:
                            message = str(e)
                            status = "error"
                        return JsonResponse({
                                'message': message,
                                'status': status
                            })
                    else:
                        message = "Semester does not exist"
                        status = "error"
                else:
                    message = "Branch does not exist"
                    status = "error"
            else:
                message = "User does not exist"
                status = "error"
        else:
            message = "Course with this code and name doesn't exists"
            status = "error"
        return JsonResponse({
                'message': message,
                'status': status
            })
    else:
        message = "We could process your request!"
        status = "error"
        return JsonResponse({
                'message':message,
                'status':status
            })

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def updateCourse(request):
    try:
        getCreatedCourseCookie = request.COOKIES['course_id']
    except Exception:
        getCreatedCourseCookie = None
    current_courseObj = None
    if getCreatedCourseCookie is not None:
        try:
            current_courseObj = CourseMC.objects.get(id=getCreatedCourseCookie)
        except CourseMC.DoesNotExist:
            current_courseObj = None
    courseExtraFields = CourseExtraFields.objects.filter(course = current_courseObj)

    try:
        getCreatedCourseCotCookie = request.COOKIES['course_cot_id']
    except Exception:
        getCreatedCourseCotCookie = None
    current_courseCOTObjs = None
    if getCreatedCourseCotCookie is not None:
        try:
            current_courseCOTObjs = CourseOfferingType.objects.get(id=getCreatedCourseCotCookie)
        except CourseOfferingType.DoesNotExist:
            current_courseCOTObjs = None
    current_courseCOTObjs = CourseOfferingType.objects.filter(course = current_courseObj)

    courseCOTExtraFields = CourseCOTExtraFields.objects.filter(course__course = current_courseObj)

    branch_list = Branch.objects.all()
    semester_list = Semester.objects.all()
    semesterModeForm = SemesterModeForm()
    courseTypeForm = CourseTypeForm()
    courseExtraFieldTypeForm = CourseExtraFieldForm()
    faculty_list = User.objects.all()
    specialization_list = SpecializationsMC.objects.all()
    prerequisiteList = CourseMC.objects.all()
    context = {
        "courseExtraFields": courseExtraFields,
        "cots": current_courseCOTObjs,
        "courseCotExtraFields": courseCOTExtraFields,
        "branch_list":branch_list,
        "semesterModeForm":semesterModeForm,
        "semester_list":semester_list,
        "faculty_list":faculty_list,
        "courseTypeForm": courseTypeForm,
        'courseExtraFieldTypeForm':courseExtraFieldTypeForm,
        "specialization_list":specialization_list,
        "prerequisiteList": prerequisiteList,
    }
    return render(request, 'course/create_course.html', context)

def createCourseExtraFieldAjax(request):
    if request.method == "POST":
        courseID = request.POST.get('course_id')
        courseExtraFieldName = request.POST.get('course_extra_field_name')
        courseExtraFieldType = request.POST.get('course_extra_field_type')

        if CourseMC.objects.filter(id = courseID).exists() is True:
            getCourseObj = CourseMC.objects.get(id = courseID)
            try:
                CourseExtraFieldsObj = CourseExtraFields.objects.create(
                    course = getCourseObj,
                    field_name = courseExtraFieldName,
                    field_type = courseExtraFieldType
                )
                courseEFObjID = CourseExtraFieldsObj.id or None
                message = "Course extra field created successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'courseEFObjID': courseEFObjID,
                'message': message, 
                'status': status
                })
        else:
            message = "Course does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def setCourseExtraFieldValueAjax(request):
    if request.method == "POST":
        courseExtraFieldID = request.POST.get('course_extra_field_id')
        courseExtraFieldValue = request.POST.get('course_extra_field_value')

        if CourseExtraFields.objects.filter(id = courseExtraFieldID).exists() is True:
            try:
                getCourseExtraFieldObj = CourseExtraFields.objects.get(id = courseExtraFieldID)
                getCourseExtraFieldObj.field_value = courseExtraFieldValue
                getCourseExtraFieldObj.save()
                message = "Data saved successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def deleteCourseExtraFieldValueAjax(request):
    if request.method == "POST":
        courseExtraFieldID = request.POST.get('course_extra_field_id')

        if CourseExtraFields.objects.filter(id = courseExtraFieldID).exists() is True:
            try:
                CourseExtraFields.objects.get(id = courseExtraFieldID).delete()
                message = "Data deleted successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def createCourseCOTAjax(request):
    if request.method == "POST":
        courseID = request.POST.get('course_cot_id')
        name = request.POST.get('mode_of_study')
        ltps = request.POST.get('course_ltps')

        if CourseMC.objects.filter(id = courseID).exists() is True:
            getCourseObj = CourseMC.objects.get(id = courseID)
            try:
                l,t,p,s = ltps.split("-")
                CourseCOTObj = CourseOfferingType.objects.create(
                    course = getCourseObj,
                    name = name,
                    l = l,
                    t = t,
                    p = p,
                    s = s
                )
                courseCOTObjID = CourseCOTObj.id or None
                message = "Course offering type extra field created successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'courseCOTObjID': courseCOTObjID,
                'message': message, 
                'status': status
                })
        else:
            message = "Course does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def setCreatedCOTFieldAjax(request):
    if request.method == "POST":
        setCreatedCOTFieldID = request.POST.get('setCreatedCOTFieldID')
        created_cot_mos_value = request.POST.get('created_cot_mos_value')
        created_cot_ltps_value = request.POST.get('created_cot_ltps_value')

        if CourseOfferingType.objects.filter(id = setCreatedCOTFieldID).exists() is True:
            try:
                l,t,p,s = created_cot_ltps_value.split("-")
                getCourseExtraFieldObj = CourseOfferingType.objects.get(id = setCreatedCOTFieldID)
                getCourseExtraFieldObj.name = created_cot_mos_value
                getCourseExtraFieldObj.l = l
                getCourseExtraFieldObj.t = t
                getCourseExtraFieldObj.p = p
                getCourseExtraFieldObj.s = s
                getCourseExtraFieldObj.save()
                message = "Data saved successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def deleteCreatedCOTFieldAjax(request):
    if request.method == "POST":
        created_cot_fieldID = request.POST.get('created_cot_field_id')

        if CourseOfferingType.objects.filter(id = created_cot_fieldID).exists() is True:
            try:
                CourseOfferingType.objects.get(id = created_cot_fieldID).delete()
                message = "Data deleted successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def getAllCurrentCOTAjax(request):
    if request.method == "POST":
        courseID = request.POST.get('course_id')
        try:
            courseIDObj = CourseMC.objects.get(id = courseID)
        except CourseMC.DoesNotExist:
            message = "Course does not exist!"
            status = "failed"
        if courseIDObj:
            message = "COT fetched successfully"
            status = "success"
            cot_list = []
            getCurrentCOTs = CourseOfferingType.objects.filter(course = courseIDObj)
            for each in getCurrentCOTs:
                cot_list.append({
                    'id': each.id,
                    'final_obj': str(each.name) + " - " + str(each.course.name)
                })
            return JsonResponse(cot_list, safe=False)
        else:
            return JsonResponse({'message': message, 'status': status})

def createCourseCOTExtraFieldAjax(request):
    if request.method == "POST":
        courseCOTID = request.POST.get('current_course_cot')
        courseExtraFieldName = request.POST.get('course_cot_extra_field_name')
        courseExtraFieldType = request.POST.get('course_cot_extra_field_type')

        if CourseOfferingType.objects.filter(id = courseCOTID).exists() is True:
            getCourseObj = CourseOfferingType.objects.get(id = courseCOTID)
            try:
                CourseCOTExtraFieldsObj = CourseCOTExtraFields.objects.create(
                    course = getCourseObj,
                    field_name = courseExtraFieldName,
                    field_type = courseExtraFieldType
                )
                courseCOTExtraFieldsObjID = CourseCOTExtraFieldsObj.id or None
                message = "Course offering type extra field created successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'courseCOTExtraFieldsObjID': courseCOTExtraFieldsObjID,
                'message': message, 
                'status': status
                })
        else:
            message = "Course does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def setCourseCOTExtraFieldValueAjax(request):
    if request.method == "POST":
        courseCOTExtraFieldID = request.POST.get('cot_extra_field_id')
        courseCOTExtraFieldValue = request.POST.get('cot_extra_field_value')

        if CourseCOTExtraFields.objects.filter(id = courseCOTExtraFieldID).exists() is True:
            try:
                getCourseCOTExtraFieldObj = CourseCOTExtraFields.objects.get(id = courseCOTExtraFieldID)
                getCourseCOTExtraFieldObj.field_value = courseCOTExtraFieldValue
                getCourseCOTExtraFieldObj.save()
                message = "Data saved successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course COT extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

def deleteCourseCOTExtraFieldValueAjax(request):
    if request.method == "POST":
        courseCOTExtraFieldID = request.POST.get('cot_extra_field_id')

        if CourseCOTExtraFields.objects.filter(id = courseCOTExtraFieldID).exists() is True:
            try:
                CourseCOTExtraFields.objects.get(id = courseCOTExtraFieldID).delete()
                message = "Data deleted successfully"
                status = "success"
            except Exception as e:
                message = e
                status = "failed"
            return JsonResponse({
                'message': message, 
                'status': status
                })
        else:
            message = "Course COT extra field does not exist!"
            status = "failed"
            return JsonResponse({'message': message, 'status': status})
    else:
        message = "Method not allowed!"
        status = "failed"
        return JsonResponse({'message': message, 'status': status})

@login_required(login_url=settings.LOGIN_URL)
def view_course(request, course_code):
    try:
        courseObj = CourseMC.objects.get(code=course_code)
        courseFilesObjs = CourseFiles.objects.filter(course = courseObj)
    except Exception:
        messages.info(request, "No such course exist")
        return redirect('manage_courses')
    faculty_list = User.objects.all()
    branch_list = Branch.objects.all()
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
            return redirect('view_course', course_code = getCourseObj.code)
        except Exception:
            messages.info(request, "Failed to create component")
            return redirect('view_course', course_code = getCourseObj.code)
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
            CourseSubComponent.objects.create(
                                            # course = getCourseObj,
                                            component = getComponentObj,
                                            name = subComponent,
                                            desc = desc)
            return redirect('view_course', course_code = getCourseObj.code)
        except Exception:
            messages.info(request, "Failed to create sub component")
            return redirect('view_course', course_code = getCourseObj.code)
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
            CourseTask.objects.create(
                                        # course = getCourseObj,
                                        # component = getComponentObj,
                                        sub_component = getSubComponentObj,
                                        question = question)
            return redirect('view_course', course_code = getCourseObj.code)
        except Exception as e:
            print(e, "Here")
            messages.info(request, "Failed to create course Task")
            return redirect('view_course', course_code = getCourseObj.code)
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
                                        # course = getCourseObj,
                                        # component = getComponentObj,
                                        # sub_component = getSubComponentObj,
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