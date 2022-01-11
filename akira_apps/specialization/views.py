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
from akira_apps.course.models import (CourseMC)
from .models import (SpecializationsMC, SpecializationFiles)
from akira_apps.academic_registration.models import (SpecEnrollStudent)

@login_required(login_url=settings.LOGIN_URL)
@allowed_users(allowed_roles=['Administrator', 'Head of the Department', 'Student'])
def manage_specializations(request):
    specializations = SpecializationsMC.objects.all()
    courses = CourseMC.objects.all()
    faculty_list = User.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    try:
        specEnrolledCurrentUserObj = SpecEnrollStudent.objects.get(user = request.user)
        specEnrolledCurrentUser = specEnrolledCurrentUserObj.enrolledSpec.id
    except Exception:
        specEnrolledCurrentUser = None
    context = {
        "specializations":specializations,
        "courses":courses,
        "faculty_list":faculty_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
        "specEnrolledCurrentUser":specEnrolledCurrentUser,
    }
    return render(request, 'specialization/manage_specializations.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_specialization_save(request):
    if request.method == 'POST':
        specializationName = request.POST.get('specialization_name')
        specializationShortInfo = request.POST.get('specialization_short_info')
        specializationWYWL = request.POST.get('specialization_wywl')
        specializationSYWG = request.POST.get('specialization_sywg')
        specializationDesc = request.POST.get('specialization_desc')
        specializationCC = request.POST.get('specialization_faculty')
        specializationCC = User.objects.get(id=specializationCC)
        specializationBranch = request.POST.get('branch')
        specializationSemester = request.POST.get('semester')
        specializationCapacity = request.POST.get('specialization_capacity')
        specializationSemester = Semester.objects.get(id=specializationSemester)
        specializationFiles = request.FILES.getlist('specialization_files')
        try:
            SpecializationsMC.objects.create(
                specialization_name=specializationName,
                specialization_short_info=specializationShortInfo,
                specialization_wywl=specializationWYWL,
                specialization_sywg=specializationSYWG,
                specialization_desc=specializationDesc,
                specialization_faculty=specializationCC,
                branch=specializationBranch,
                capacity=specializationCapacity)
            getSpecializationObj = SpecializationsMC.objects.get(specialization_name = specializationName)
            if specializationFiles:
                try:
                    for file in specializationFiles:
                        SpecializationFiles.objects.create(specialization = getSpecializationObj, specialization_files = file)
                    messages.success(request, "Specialization created successfully")
                except Exception as e:
                    messages.error(request, e)
        except Exception as e:
            messages.error(request, e)
        return redirect('manage_specializations')

@login_required(login_url=settings.LOGIN_URL)
def view_specialization(request, specialization_name):
    specializationObj = SpecializationsMC.objects.get(specialization_name=specialization_name)
    specializationFilesObjs = SpecializationFiles.objects.filter(specialization = specializationObj)
    faculty_list = User.objects.all()
    branch_list = BranchForm()
    semester_list = Semester.objects.all()
    edit_course = False
    try:
        specEnrolledCurrentUserObj = SpecEnrollStudent.objects.get(user = request.user)
        specEnrolledCurrentUser = specEnrolledCurrentUserObj.enrolledSpec.id
    except Exception:
        specEnrolledCurrentUser = None
    context = {
        "specialization":specializationObj,
        "specializationFilesObjs":specializationFilesObjs,
        "faculty_list":faculty_list,
        "branch_list":branch_list,
        "semester_list":semester_list,
        "edit_course":edit_course,
        "specEnrolledCurrentUser":specEnrolledCurrentUser,
    }
    return render(request, 'specialization/view_specialization.html', context)

@login_required(login_url=settings.LOGIN_URL)
def search_specialization(request):
    if request.method == 'POST':
        query = request.POST['search-specialization'].strip()
        try:
            specEnrolledCurrentUserObj = SpecEnrollStudent.objects.get(user = request.user)
            specEnrolledCurrentUser = specEnrolledCurrentUserObj.enrolledSpec.id
        except Exception:
            specEnrolledCurrentUser = None
        beforeSearch = datetime.now()
        specializations = SpecializationsMC.objects.filter(
            Q(specialization_name__icontains=query) |
            Q(specialization_short_info__icontains=query) | Q(specialization_wywl__icontains=query) |
            Q(specialization_sywg__icontains=query) | Q(specialization_desc__icontains=query) |
            Q(specialization_faculty__first_name__icontains=query) | Q(specialization_faculty__last_name__icontains=query) |
            Q(branch__icontains=query)
        )
        afterSearch = datetime.now()
        totalTimeTaken = (afterSearch - beforeSearch).total_seconds()
        context = {
            'specializations': specializations,
            'totalTimeTaken':totalTimeTaken,
            'query':query,
            'specEnrolledCurrentUser':specEnrolledCurrentUser,
        }
        return render(request, 'specialization/search_specializations.html', context)
    else:
        messages.info(request, "We could process your request!")
        return redirect('manage_specializations')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_specialization(request, specialization_id):
    specialization = SpecializationsMC.objects.get(id=specialization_id)
    specialization.delete()
    return redirect('manage_specializations')