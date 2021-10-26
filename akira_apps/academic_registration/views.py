from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from akira_apps.academic_registration.forms import BranchForm, SectionRoomForm, SemesterForm
from akira_apps.academic_registration.models import Block, SectionRooms, Semester, Specialization, specialization_registration_staff, specialization_registration_student
from akira_apps.staff.models import Staffs

def create_block(request):
    formType = "Create Block"
    context = {
        "formType":formType,
    }
    return render(request, 'academic_registration/block/create_edit_block.html', context)

def create_block_save(request):
    if request.method == 'POST':
        blockName = request.POST.get('block_name').upper()
        try:
            block = Block(block_name=blockName)
            block.save()
            return redirect('manage_block')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request Now...!")

def edit_block(request, block_id):
    current_block = Block.objects.get(id=block_id)
    formType = "Edit Block"
    context = {
        "current_block":current_block,
        "formType":formType,
    }
    return render(request, 'academic_registration/block/create_edit_block.html', context)


def edit_block_save(request, block_id):
    if request.method == 'POST':
        blockName = request.POST.get('block_name').upper()
        try:
            block = Block.objects.get(id=block_id)
            block.block_name=blockName
            block.save()
            return redirect('manage_block')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request Now...!")

def delete_block(request, block_id):
    try:
        current_block = Block.objects.get(id=block_id)
        current_block.delete()
        return redirect('manage_block')
    except Exception as e:
        return HttpResponse(e)

def manage_block(request):
    block_list = Block.objects.all()
    context = {
        "block_list":block_list,
    }
    return render(request, 'academic_registration/block/manage_block.html', context)

def create_section_room(request):
    block_name_list = Block.objects.all()
    if len(block_name_list) == 0:
        message = "First You Need To Create Block"
        print(message)
        return redirect('manage_block')
    else:
        sectionRoomForm = SectionRoomForm()
        formType = "Create Section Room"
        context = {
            "sectionRoomForm":sectionRoomForm,
            "block_name_list":block_name_list,
            "formType":formType
        }
        return render(request, 'academic_registration/section_room/create_edit_section_room.html', context)

def create_section_room_save(request):
    if request.method == 'POST':
        sectionName = request.POST.get('section_name')
        roomNo = request.POST.get('room_no')
        floorNo = request.POST.get('floor_no')
        blockName = request.POST.get('block_name')
        capacityRoom = request.POST.get('capacity_room')
        blockName_id = Block.objects.get(id=blockName)
        try:
            sectionRoom = SectionRooms(section_name=sectionName, room_no=roomNo, floor=floorNo, block=blockName_id, capacity=capacityRoom)
            sectionRoom.save()
            return redirect('manage_section_room')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request Now...!")

def edit_section_room(request, section_room_id):
    sectionRoomForm = SectionRoomForm()
    block_name_list = Block.objects.all()
    section_room_list = SectionRooms.objects.all()
    current_section_room = SectionRooms.objects.get(id=section_room_id)
    context = {
        "sectionRoomForm":sectionRoomForm,
        "block_name_list":block_name_list,
        "section_room_list":section_room_list,
        "current_section_room":current_section_room,
    }
    return render(request, 'academic_registration/section_room/create_edit_section_room.html', context)

def edit_section_room_save(request, section_room_id):
    if request.method == 'POST':
        sectionName = request.POST.get('section_name')
        roomNo = request.POST.get('room_no')
        floorNo = request.POST.get('floor_no')
        blockName = request.POST.get('block_name')
        capacityRoom = request.POST.get('capacity_room')
        blockName_id = Block.objects.get(id=blockName)
        try:
            sectionRoom = SectionRooms.objects.get(id=section_room_id)
            sectionRoom.section_name=sectionName
            sectionRoom.room_no=roomNo
            sectionRoom.floor=floorNo
            sectionRoom.block=blockName_id
            sectionRoom.capacity=capacityRoom
            sectionRoom.save()
            return redirect('manage_section_room')
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Couldn't Make Your Request Now...!")

def delete_section_room(request, section_room_id):
    try:
        sectionRoom = SectionRooms.objects.get(id=section_room_id)
        sectionRoom.delete()
        return redirect('manage_section_room')
    except Exception as e:
        return HttpResponse(e)

def manage_section_room(request):
    section_room_list = SectionRooms.objects.all()
    context = {
        "section_room_list":section_room_list,
    }
    return render(request, 'academic_registration/section_room/manage_section_room.html', context)

def manage_semester(request):
    semesterForm = SemesterForm()
    semester_list = Semester.objects.all()
    typeform = "create"
    context = {
        "semesterForm":semesterForm,
        "semester_list":semester_list,
        "typeform":typeform
    }
    return render(request, 'academic_registration/semester/manage_semester.html', context)

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
    return redirect('manage_semester')

def edit_semester(request, semester_id):
    semesterForm = SemesterForm()
    semester_data = Semester.objects.get(id=semester_id)
    semester_list = Semester.objects.all()
    typeform = "edit"
    context = {
        "semesterForm":semesterForm,
        "semester_data":semester_data,
        "semester_list":semester_list,
        "typeform":typeform
    }
    return render(request, 'academic_registration/semester/manage_semester.html', context)

def save_edit_semester(request, semester_id):
    if request.method == 'POST':
        semesterMode = request.POST.get('mode')
        startYear = request.POST.get('start_year')
        endYear = request.POST.get('end_year')
        if request.POST.get('semester_status') == 'on':
            semesterStatus = True
        else:
            semesterStatus = False
        try:
            semester = Semester.objects.get(id=semester_id)
            semester.mode=semesterMode
            semester.start_year=startYear
            semester.end_year=endYear
            semester.is_active=semesterStatus
            semester.save()
        except Exception as e:
            return HttpResponse(e)
    return redirect('manage_semester')

def delete_semester(request, semester_id):
    try:
        semester = Semester.objects.get(id=semester_id)
        semester.delete()
        return redirect('manage_semester')
    except Exception as e:
        return HttpResponse(e)

# all_section_room_list = SectionRooms.objects.all()
# for i in all_section_room_list:
#     sectionRoom = SectionRooms.objects.get(id=i.id)
#     sectionRoom.delete()

from itertools import chain
def create_specialization(request):
    branchForm = BranchForm()
    if Staffs.objects.all().count() == 0:
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