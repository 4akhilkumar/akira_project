from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from akira_apps.academic_registration.forms import SemesterForm

from akira_apps.academic_registration.models import Semester

# Create your views here.
def create_semester(request):
    semesterForm = SemesterForm()
    context = {
        "semesterForm":semesterForm,
    }
    return render(request, 'academic_registration/Semester/create_semester.html', context)

def save_created_semester(request):
    if request.method == 'POST':
        semesterMode = request.POST.get('mode')
        startYear = request.POST.get('start_year')
        endYear = request.POST.get('end_year')
        if request.POST.get('semester_status') == 'on':
            semesterStatus = True
        else:
            semesterStatus = False
        try:
            semester = Semester(mode=semesterMode, start_year=startYear, end_year=endYear, is_active=semesterStatus)
            semester.save()
        except Exception as e:
            return HttpResponse(e)
    return redirect('create_semester')