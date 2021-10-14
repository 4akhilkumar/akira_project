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
    return render(request, 'academic_registration/section_room/create_section_room.html', context)

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
