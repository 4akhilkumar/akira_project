from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from akira_apps.academic_registration.forms import SectionRoomForm
from akira_apps.staff.models import Staff

from itertools import chain

def sem_registration(request):
    return render(request, 'academic_registration/sem_registration.html')

def create_specialization(request):
    branchForm = BranchForm()
    if Staff.objects.all().count() == 0:
        return redirect('add_staff')

    hod_list = User.objects.filter(groups__name='Head of the Department')
    course_coordinator_list = User.objects.filter(groups__name='Course Co-Ordinator')
    staff_list = User.objects.filter(groups__name='Course Co-Ordinator').filter(groups__name='Staff')
    faculty_list = list(chain(hod_list, course_coordinator_list, staff_list))

    formType = "Create Specialization"
    context = {
        "branchForm":branchForm,
        "faculty_list":faculty_list,
        "formType":formType,
    }
    return render(request, 'academic_registration/specialization/create_edit_specialization.html', context)

def create_specialization_save(request):
    if request.method == 'POST':
        specializationName = request.POST.get('specialization_name').strip()
        specializationShortInfo = request.POST.get('specialization_short_info').strip()
        specializationWywl = request.POST.get('specialization_wywl').strip()
        specializationSywg = request.POST.get('specialization_sywg').strip()
        specializationDesc = request.POST['specialization_desc']
        facultySpec = request.POST.get('faculty')
        faculty_id = User.objects.get(id=facultySpec)
        branch_name = request.POST.get('branch')
        specCapacity = request.POST.get('specCapacity')
        try:
            specialization = Specialization(specialization_name=specializationName, 
                            specialization_short_info=specializationShortInfo, 
                            specialization_wywl=specializationWywl, 
                            specialization_sywg=specializationSywg, 
                            specialization_desc=specializationDesc, 
                            specialization_faculty=faculty_id,
                            branch=branch_name,
                            capacity=specCapacity)
            specialization.save()
            return redirect('manage_specialization')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

def edit_specialization(request, specialization_id):
    branchForm = BranchForm()
    specialization = Specialization.objects.get(id=specialization_id)
    hod_list = User.objects.filter(groups__name='Head of the Department')
    course_coordinator_list = User.objects.filter(groups__name='Course Co-Ordinator')
    staff_list = User.objects.filter(groups__name='Course Co-Ordinator').filter(groups__name='Staff')
    faculty_list = list(chain(hod_list, course_coordinator_list, staff_list))
    context = {
        "branchForm":branchForm,
        "specialization":specialization,
        "faculty_list":faculty_list,
    }
    return render(request, 'academic_registration/specialization/create_edit_specialization.html', context)

def edit_specialization_save(request, specialization_id):
    if request.method == 'POST':
        specializationName = request.POST.get('specialization_name').strip()
        specializationShortInfo = request.POST.get('specialization_short_info').strip()
        specializationWywl = request.POST.get('specialization_wywl').strip()
        specializationSywg = request.POST.get('specialization_sywg').strip()
        specializationDesc = request.POST['specialization_desc']
        facultySpec = request.POST.get('faculty')
        faculty_id = User.objects.get(id=facultySpec)
        branch_name = request.POST.get('branch')
        specCapacity = request.POST.get('specCapacity')

        try:
            specialization = Specialization.objects.get(id=specialization_id)
            specialization.specialization_name=specializationName 
            specialization.specialization_short_info=specializationShortInfo 
            specialization.specialization_wywl=specializationWywl 
            specialization.specialization_sywg=specializationSywg 
            specialization.specialization_desc=specializationDesc 
            specialization.specialization_faculty=faculty_id
            specialization.branch=branch_name
            specialization.capacity=specCapacity
            specialization.save()
            return redirect('manage_specialization')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't make your request...!")

def delete_specialization(request, specialization_id):
    try:
        specialization = Specialization.objects.get(id=specialization_id)
        specialization.delete()
        return redirect('manage_specialization')
    except Exception as e:
        return HttpResponse(e)

def view_specialization(request, specialization_id):
    specialization = Specialization.objects.get(id=specialization_id)
    
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all()))

    staff_enrolled_specialization = specialization_registration_staff.objects.filter(specialization=specialization.id, staff=request.user.id)
    staff_specialization_id_list = []
    for i in staff_enrolled_specialization:
        specialization_object = specialization_registration_staff.objects.get(id=i.id, staff=request.user.id)
        specialization_id = specialization_registration_staff.objects.get(id=specialization_object.id)
        staff_specialization_id_list.append(str(specialization_id.specialization.id))
    staff_specialization_id_list_str = ", ".join(staff_specialization_id_list)

    student_enrolled_specialization = specialization_registration_student.objects.filter(specialization=specialization.id, student=request.user.id)
    student_specialization_id_list = []
    for i in student_enrolled_specialization:
        specialization_object = specialization_registration_student.objects.get(id=i.id, student=request.user.id)
        specialization_id = specialization_registration_student.objects.get(id=specialization_object.id)
        student_specialization_id_list.append(str(specialization_id.specialization.id))
    student_specialization_id_list_str = ", ".join(student_specialization_id_list)

    enrolled_staff = specialization_registration_staff.objects.filter(specialization=specialization.id)
    staff_specialization_enrolled_list = []
    for i in enrolled_staff:
        staff_specialization_enrolled_list.append(i.staff)
    staff_specialization_enrolled_list_set = [i for n, i in enumerate(staff_specialization_enrolled_list) if i not in staff_specialization_enrolled_list[:n]]

    enrolled_students = specialization_registration_student.objects.filter(specialization=specialization.id)
    student_course_enrolled_list = []
    for i in enrolled_students:
        student_course_enrolled_list.append(i.student)

    context = {
        "view_specialization":specialization,
        "group_list":group_list,
        "staff_specialization_id_list_str":staff_specialization_id_list_str,
        "student_specialization_id_list_str":student_specialization_id_list_str,
        "staff_specialization_enrolled_list_set":staff_specialization_enrolled_list_set,
        "student_course_enrolled_list":student_course_enrolled_list,
    }
    return render(request, 'academic_registration/specialization/view_specialization.html', context)

def manage_specialization(request):
    specialization_list = Specialization.objects.all()
    user = User.objects.get(id=request.user.id)
    group_list = ', '.join(map(str, user.groups.all()))
    context = {
        "specialization_list":specialization_list,
        "group_list":group_list,
    }
    return render(request, 'academic_registration/specialization/manage_specialization.html', context)

def staff_enroll_specialization(request, specialization_id):
    current_staff = User.objects.get(id=request.user.id)
    specializationId = Specialization.objects.get(id=specialization_id)
    try:
        enroll_specialization = specialization_registration_staff(staff = current_staff, specialization = specializationId)
        enroll_specialization.save()
        return redirect('manage_specialization')
    except Exception as e:
        return HttpResponse(e)

def student_enroll_specialization(request, specialization_id):
    current_student = User.objects.get(id=request.user.id)
    specializationId = Specialization.objects.get(id=specialization_id)
    specializationCapacity = specializationId.capacity - 1
    print(specializationCapacity)

    try:
        enroll_specialization = specialization_registration_student(student = current_student, specialization = specializationId)
        enroll_specialization.save()
        current_specialization = Specialization.objects.get(id=specialization_id)
        current_specialization.capacity=specializationCapacity
        current_specialization.save()
        return redirect('manage_specialization')
    except Exception as e:
        return HttpResponse(e)

def student_unenroll_specialization(request, specialization_id):
    current_student = User.objects.get(id=request.user.id)
    specializationId = Specialization.objects.get(id=specialization_id)
    specializationCapacity = specializationId.capacity + 1

    try:

        enroll_specialization = specialization_registration_student.objects.filter(student = current_student, specialization = specializationId)
        enroll_specialization.delete()
        current_specialization = Specialization.objects.get(id=specialization_id)
        current_specialization.capacity=specializationCapacity
        current_specialization.save()
        return redirect('manage_specialization')
    except Exception as e:
        return HttpResponse(e)

# student_unenroll_specialization = specialization_registration_student.objects.all()
# for i in student_unenroll_specialization:
#     unenroll_specialization = specialization_registration_student.objects.get(id=i.id)
#     unenroll_specialization.delete()