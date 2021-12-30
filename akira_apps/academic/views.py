from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse

from akira_apps.super_admin.decorators import allowed_users
from .models import (Semester, Block, Floor, Room)
from akira_apps.academic.forms import (RoomTypeForm, SemesterModeForm)

def returnBlockName(blockName):
    if not "block" in blockName:
        blockName = blockName.capitalize() + " Block"
    if "block" in blockName.lower() and " " not in blockName[:blockName.lower().index("block")]:
        if "-" not in blockName[:blockName.lower().index("block")]:
            blockName = blockName.replace("block", " Block")
    if " " in blockName:
        splitbyspace = blockName.split(" ")
        splitbyspace = [x.capitalize() for x in splitbyspace]
        blockName = "-".join(splitbyspace)
    if "," in blockName:
        splitbycomma = blockName.split(",")
        splitbycomma = [x.capitalize() for x in splitbycomma]
        blockName = ",".join(splitbycomma)
    if "#" in blockName:
        splitbyhash = blockName.split("#")
        splitbyhash = [x.capitalize() for x in splitbyhash]
        blockName = "#".join(splitbyhash)
    if "-" in blockName:
        splitbydash = blockName.split("-")
        splitbydash = [x.capitalize() for x in splitbydash]
        blockName = "-".join(splitbydash)
    if "&" in blockName:
        splitbyampersand = blockName.split("&")
        splitbyampersand = [x.capitalize() for x in splitbyampersand]
        blockName = "&".join(splitbyampersand)
    if "block" in blockName:
        blockName = blockName.replace("block", " Block")
    return blockName

@allowed_users(allowed_roles=['Administrator'])
def create_block_save(request):
    if request.method == 'POST':
        blockName = request.POST.get('block_name')
        if "block" == blockName.lower() or blockName == None or blockName == "":
            messages.info(request, 'What BLock is it?')
            return redirect('manage_academic')
        getblockName = returnBlockName(blockName)
        blockDesc = request.POST.get('block_desc')
        try:
            Block.objects.create(block_name=getblockName, block_desc=blockDesc)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messages.info(request, 'Block Name Already Exists!')
                return redirect('manage_academic')
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def delete_block(request, block_id):
    block = Block.objects.get(id = block_id)
    block.delete()
    return redirect('manage_academic')

def ordinal(n):
    s = ('th', 'st', 'nd', 'rd') + ('th',)*10
    v = n%100
    if v > 13:
        return f'{n}{s[v%10]}'
    else:
        return f'{n}{s[v]}'

def returnFloorName(floorName):
    if floorName.isnumeric():
        floorName = ordinal(int(floorName)) + " Floor"
    if " " in floorName:
        splitbyspace = floorName.split(" ")
        splitbyspace = [x.capitalize() for x in splitbyspace]
        floorName = " ".join(splitbyspace)
    if " " not in floorName[:floorName.lower().index("floor")]:
        floorName = floorName.replace("floor", " Floor")
    if any(char.isdigit() for char in floorName):
        for i, char in enumerate(floorName):
            if char.isdigit():
                floorName = ordinal(int(floorName[i])) + " Floor"
                break
    return floorName

@allowed_users(allowed_roles=['Administrator'])
def create_floor_save(request):
    if request.method == 'POST':
        floorName = request.POST.get('floor_name')
        floorName = returnFloorName(floorName)
        blockID = request.POST.get('block_id')
        fetechBlock = Block.objects.get(id = blockID)
        try:
            Floor.objects.create(floor_name = floorName, block = fetechBlock)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messages.info(request, '{} Already Exists in {}!'.format(floorName, fetechBlock.block_name))
                return redirect('manage_academic')
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def delete_floor(request, floor_id):
    floor = Floor.objects.get(id = floor_id)
    floor.delete()
    return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def getFloorbyBlock(request):
    if request.method == "POST":
        block_id = request.POST['block']
        try:
            blockObj = Block.objects.get(id = block_id)
            getFloors = Floor.objects.filter(block__block_name=blockObj.block_name)
            print(getFloors)
        except Exception as e:
            print(e)
        return JsonResponse(list(getFloors.values('id', 'floor_name')), safe = False) 

@allowed_users(allowed_roles=['Administrator'])
def create_room_save(request):
    if request.method == 'POST':
        roomName = request.POST.get('room_name')
        roomBlockID = request.POST.get('get_block_id')
        fetchedBlock = Block.objects.get(id = roomBlockID)
        roomFloorID = request.POST.get('floor_id')
        fetchedFloor = Floor.objects.get(id = roomFloorID)
        roomCapacity = request.POST.get('capacity')
        roomType = request.POST.get('room_type')
        try:
            Room.objects.create(room_name=roomName,
                                block=fetchedBlock,
                                floor=fetchedFloor,
                                type=roomType,
                                capacity=roomCapacity)
        except Exception as e:
            print(e)
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def delete_room(request, room_id):
    room = Room.objects.get(id = room_id)
    room.delete()
    return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def create_semester_save(request):
    if request.method == 'POST':
        semesterMode = request.POST.get('semester_mode')
        semesterStartYear = request.POST.get('semester_start_year')
        semesterEndYear = request.POST.get('semester_end_year')
        semesterisActive = request.POST.get('semester_is_active')
        if semesterisActive == 'on':
            semesterisActive = True
        else:
            semesterisActive = False
        createSemester = Semester.objects.create(mode=semesterMode,
                                                start_year=semesterStartYear,
                                                end_year=semesterEndYear,
                                                is_active=semesterisActive)
        createSemester.save()
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def fetch_semester(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    context = {
        'semester': semester
    }
    return render(request, 'academic/semester/edit_semester.html', context)

@allowed_users(allowed_roles=['Administrator'])
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
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator'])
def delete_semester(request, semester_id):
    semester = Semester.objects.get(id = semester_id)
    semester.delete()
    return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def manage_academic(request):
    blocks = Block.objects.all().order_by('block_name')
    floors = Floor.objects.all()
    rooms = Room.objects.all()
    roomTypeForm = RoomTypeForm()
    semesters = Semester.objects.all()
    semesterModeForm = SemesterModeForm()
    getActiveSemester = Semester.objects.filter(is_active=True)
    activeSemesterMode = "--"
    if getActiveSemester:
        activeSemesterMode = getActiveSemester[0].mode
    context = {
        "blocks": blocks,
        "floors": floors,
        "rooms": rooms,
        "roomTypeForm":roomTypeForm,
        "semesters":semesters,
        "semesterModeForm":semesterModeForm,
        "activeSemesterMode":activeSemesterMode,
    }
    return render(request, 'academic/academic.html', context)