from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from akira_apps.adops.models import AdmissionRegister

from akira_apps.super_admin.decorators import (allowed_users)
from akira_apps.academic.models import (Semester, Branch)
from akira_apps.academic.forms import (SemesterModeForm)
from akira_apps.academic_registration.models import (SetSemesterRegistration)

def aca_Registration(request):
    branches = Branch.objects.all()
    semesters = Semester.objects.all().order_by('-is_active')
    semesterModeForm = SemesterModeForm()
    getActiveSemesters = Semester.objects.filter(is_active=True)
    context = {
        "branches": branches,
        "semesters":semesters,
        "semesterModeForm":semesterModeForm,
        "getActiveSemesters":getActiveSemesters,
    }
    return render(request, 'academic_registration/acaRegistration.html', context)

def getAllBranchesAjax(request):
    getBranches = Branch.objects.all()
    return JsonResponse(list(getBranches.values('id', 'name')), safe = False)

@allowed_users(allowed_roles=['Administrator', 'Teaching Staff', 'Adops Team'])
def createbranchAjax(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        if Branch.objects.filter(name__contains = name).exists() is False:
            Branch.objects.create(name = name, description = desc)
            message = "Branch %s created successfully!" % str(name)
            status = "success"
        else:
            message = "Branch %s already exists!" % str(name)
            status = "failed"
        return JsonResponse({
            'message': message,
            'status': status
            }, safe = False)
    else:
        return JsonResponse({'message': "Invalid request"}, safe = False)

@allowed_users(allowed_roles=['Administrator', 'Teaching Staff', 'Adops Team'])
def createbranch(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        if Branch.objects.filter(name__contains = name).exists() is False:
            Branch.objects.create(name = name, description = desc)
            messages.success(request, "Branch %s created successfully!" % str(name))
        else:
            messages.info(request, "Branch %s already exists!" % str(name))
    return redirect('aca_Registration')

def getAllSemestersAjax(request):
    getSemesters = Semester.objects.all()
    return JsonResponse(list(getSemesters.values('id', 'mode', 'start_year', 'end_year', 'branch__name', 'is_active')), safe = False)

@allowed_users(allowed_roles=['Administrator', 'Teaching Staff'])
def createsemesterAjax(request):
    if request.method == "POST":
        semesterMode = request.POST.get('mode')
        semesterStartYear = request.POST.get('start_year')
        semesterEndYear = request.POST.get('end_year')
        semesterBranch = request.POST.get('branch')
        try:
            semesterBranch = Branch.objects.get(id=semesterBranch)
        except Branch.DoesNotExist:
            message = "Branch does not exist!"
            status = "failed"
        semesterisActive = request.POST.get('is_active')
        if semesterisActive == 'on':
            semesterisActive = True 
        else:
            semesterisActive = False
        if Semester.objects.filter(mode=semesterMode, start_year=semesterStartYear, end_year=semesterEndYear, branch = semesterBranch).exists() is False:
            Semester.objects.create(mode=semesterMode, start_year=semesterStartYear,
                                    end_year=semesterEndYear, branch = semesterBranch,
                                    is_active=semesterisActive)
            message = "Semester created successfully!"
            status = "success"
        else:
            message = "{} Semester {} already exists!".format(str(semesterMode), str(semesterStartYear))
            status = "failed"
        return JsonResponse({
            'message': message,
            'status': status
            }, safe = False)
    else:
        return JsonResponse({'message': "Invalid request"}, safe = False)

@allowed_users(allowed_roles=['Administrator', 'Teaching Staff'])
def createsemester(request):
    if request.method == "POST":
        semesterMode = request.POST.get('semester_mode')
        semesterStartYear = request.POST.get('start_year')
        semesterEndYear = request.POST.get('end_year')
        semesterBranch = request.POST.get('branch')
        try:
            semesterBranch = Branch.objects.get(id=semesterBranch)
        except Branch.DoesNotExist:
            messages.error(request, "Branch does not exist!")
            messages.info(request, "Please create a branch")
            return redirect('manage_academic')
        semesterisActive = request.POST.get('semester_is_active')
        if semesterisActive == 'on':
            semesterisActive = True 
        else:
            semesterisActive = False
        if Semester.objects.filter(mode=semesterMode, start_year=semesterStartYear, end_year=semesterEndYear, branch = semesterBranch).exists() is False:
            Semester.objects.create(mode=semesterMode, start_year=semesterStartYear,
                                    end_year=semesterEndYear, branch = semesterBranch,
                                    is_active=semesterisActive)
            messages.success(request, "Semester created successfully!")
            return redirect('aca_Registration')
        else:
            messages.info(request, "{} Semester {} already exists!".format(str(semesterMode), str(semesterStartYear)))
    return redirect('aca_Registration')


def setTeachingStaffSemesterRegistrationAjax(request):
    if request.method == "POST":
        semesterId = request.POST.get('semester_id')
        if Semester.objects.filter(id=semesterId).exists() is True:
            semesterObj = Semester.objects.get(id=semesterId)
            try:
                getSemesterStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
            except SetSemesterRegistration.DoesNotExist:
                getSemesterStatus = SetSemesterRegistration.objects.create(semester = semesterObj, teachingstaff = True)
                message = "Semester registration status set successfully!"
                status = "success"
            if getSemesterStatus.teachingstaff is True:
                getSemesterStatus.teachingstaff = False
                getSemesterStatus.save()
                message = "Semester registration status changed successfully!"
                status = "success"
            else:
                getSemesterStatus.teachingstaff = True
                getSemesterStatus.save()
                message = "Semester registration status changed successfully!"
                status = "success"
        else:
            message = "Semester does not exist!"
            status = "error"
        return JsonResponse({'message': message, 'status': status}, safe = False)

def setStudentSemesterRegistrationAjax(request):
    if request.method == "POST":
        semesterId = request.POST.get('semester_id')
        if Semester.objects.filter(id=semesterId).exists() is True:
            semesterObj = Semester.objects.get(id=semesterId)
            try:
                getSemesterStatus = SetSemesterRegistration.objects.get(semester = semesterObj)
            except SetSemesterRegistration.DoesNotExist:
                getSemesterStatus = SetSemesterRegistration.objects.create(semester = semesterObj, students = True)
                message = "Semester registration status set successfully!"
                status = "success"
            if getSemesterStatus.students is True:
                getSemesterStatus.students = False
                getSemesterStatus.save()
                message = "Semester registration status changed successfully!"
                status = "success"
            else:
                getSemesterStatus.students = True
                getSemesterStatus.save()
                message = "Semester registration status changed successfully!"
                status = "success"
        else:
            message = "Semester does not exist!"
            status = "error"
        return JsonResponse({'message': message, 'status': status}, safe = False)

def studentAcaReg(request):
    if AdmissionRegister.objects.filter(user = request.user).exists() is True:
        admissionInfo = AdmissionRegister.objects.get(user = request.user)
    context = {
        "admissionInfo": admissionInfo,
    }
    return render(request, 'academic_registration/studentAcademyReg.html', context)