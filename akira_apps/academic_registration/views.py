from django.contrib import messages
from django.shortcuts import redirect, render

from akira_apps.specialization.models import (SpecializationsMC)
from akira_apps.academic_registration.models import (SpecEnrollStudent)

def sem_registration(request):
    return render(request, 'academic_registration/semRegistration.html')

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