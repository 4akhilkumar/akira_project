from django.contrib import messages
from django.shortcuts import redirect, render

from akira_apps.super_admin.decorators import allowed_users
from akira_apps.academic.models import (Semester, Branch)
from akira_apps.academic.forms import (SemesterModeForm)
from akira_apps.specialization.models import (SpecializationsMC)
from akira_apps.academic_registration.models import (SpecEnrollStudent)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_semester_save(request):
    if request.method == 'POST':
        semesterMode = request.POST.get('semester_mode')
        semesterStartYear = request.POST.get('semester_start_year')
        semesterEndYear = request.POST.get('semester_end_year')
        semesterBranch = request.POST.get('branch')
        semesterisActive = request.POST.get('semester_is_active')
        if semesterisActive == 'on':
            semesterisActive = True
        else:
            semesterisActive = False
        createSemester = Semester.objects.create(mode=semesterMode,
                                                start_year=semesterStartYear,
                                                end_year=semesterEndYear,
                                                branch = semesterBranch,
                                                is_active=semesterisActive)
        createSemester.save()
        return redirect('sem_registration')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def fetch_semester(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    context = {
        'semester': semester
    }
    return render(request, 'academic/semester/edit_semester.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def update_semester_save(request, semester_id):
    if request.method == 'POST':
        semesterMode = request.POST.get('semester_mode')
        semesterStartYear = request.POST.get('semester_start_year')
        semesterEndYear = request.POST.get('semester_end_year')
        semesterisActive = request.POST.get('semester_is_active')
        if semesterisActive == 'on':
            semesterisActive = True
        else:
            semesterisActive = False
        updateSemester = Semester.objects.get(id = semester_id)
        updateSemester.mode=semesterMode
        updateSemester.start_year=semesterStartYear
        updateSemester.end_year=semesterEndYear
        updateSemester.is_active=semesterisActive
        updateSemester.save()
        return redirect('sem_registration')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_semester(request, semester_id):
    semester = Semester.objects.get(id = semester_id)
    semester.delete()
    return redirect('sem_registration')

def enrollSpec(request, speci_id):
    if request.method == "POST":
        getSpecObj = SpecializationsMC.objects.get(id=speci_id)
        if getSpecObj.capacity != 0:
            try:
                SpecEnrollStudent.objects.create(user = request.user, enrolledSpec = getSpecObj)
                getSpecObj.capacity -= 1
                getSpecObj.save()
                messages.success(request, "You have enrolled successfully")
            except Exception:
                messages.info(request, "You have already enrolled")
        else:
            messages.info(request, "Sorry, Enroll for %s is Closed" % (getSpecObj.specialization_name))
    return redirect('manage_specializations')

def unenrollSpec(request, speci_id):
    if request.method == "POST":
        getSpecObj = SpecializationsMC.objects.get(id=speci_id)
        try:
            SpecEnrollStudent.objects.get(user = request.user, enrolledSpec = getSpecObj).delete()
            getSpecObj.capacity += 1
            getSpecObj.save()
            messages.success(request, "You have Unenrolled successfully")
        except Exception:
            messages.info(request, "You have already Unenrolled")
    return redirect('manage_specializations')

def sem_registration(request):
    branch_list = Branch.objects.all()
    semesters = Semester.objects.all()
    semesterModeForm = SemesterModeForm()
    getActiveSemester = Semester.objects.filter(is_active=True)
    activeSemesterMode = "--"
    if getActiveSemester:
        activeSemesterMode = getActiveSemester[0].mode
    context = {
        "branch_list":branch_list,
        "semesters":semesters,
        "semesterModeForm":semesterModeForm,
        "activeSemesterMode":activeSemesterMode,
    }
    return render(request, 'academic_registration/semRegistration.html', context)