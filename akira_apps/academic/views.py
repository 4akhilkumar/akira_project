from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse

import pandas as pd
import io
import csv
import datetime as pydt

from akira_apps.super_admin.decorators import allowed_users
from .models import (Block, Floor, Room, Branch)
from akira_apps.academic.forms import (RoomTypeForm)

def getAllBranches(request):
    getBranches = Branch.objects.all()
    return JsonResponse(list(getBranches.values('id', 'name')), safe = False)

def add_branch(request):
    if request.method == "POST":
        name = request.POST.get('branch')
        save = request.POST.get('_save')
        addanother = request.POST.get('_addanother')
        if Branch.objects.filter(name = name).exists() is False:
            branchObj = Branch.objects.create(name = name)            
            if save:
                return redirect('manage_branches')
            elif addanother:
                return redirect('add_branch')
            else:
                return redirect('edit_branch', stdID = branchObj.id)
        else:
            messages.info(request, "%s already exists!" % str(name))
            return redirect('add_branch')
    return render(request, "academic/manage_branches/add_branch.html")

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_block(request):
    if request.method == 'POST':
        blockName = request.POST.get('name')
        if "block" == blockName.lower() or blockName == None or blockName == "":
            messages.info(request, 'What Block is it?')
            return redirect('manage_academic')
        blockDesc = request.POST.get('desc')
        try:
            Block.objects.create(name=blockName, desc=blockDesc)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messages.info(request, 'Block Name Already Exists!')
            else:
                messages.info(request, e)
            return redirect('manage_academic')
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
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
    if any(char.isdigit() for char in floorName):
        for i, char in enumerate(floorName):
            if char.isdigit():
                floorName = ordinal(int(floorName[i])) + " Floor"
                break
    return floorName

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_floor(request):
    if request.method == 'POST':
        floorName = request.POST.get('name')
        floorName = returnFloorName(floorName)
        blockID = request.POST.get('block_id')
        fetechBlock = Block.objects.get(id = blockID)
        try:
            Floor.objects.create(name = floorName, block = fetechBlock)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                messages.info(request, '{} Already Exists in {}!'.format(floorName, fetechBlock.name))
            else:
                messages.info(request, e)
            return redirect('manage_academic')
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_floor(request, floor_id):
    floor = Floor.objects.get(id = floor_id)
    floor.delete()
    return redirect('manage_academic')

def getFloorbyBlock(request):
    if request.method == "POST":
        block_id = request.POST['block']
        try:
            blockObj = Block.objects.get(id = block_id)
            getFloors = Floor.objects.filter(block__name=blockObj.name)
        except Exception as e:
            return JsonResponse(list({'error': str(e)}), safe = False)
        return JsonResponse(list(getFloors.values('id', 'name')), safe = False) 

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_room_save(request):
    if request.method == 'POST':
        roomName = request.POST.get('name')
        roomBlockID = request.POST.get('get_block_id')
        fetchedBlock = Block.objects.get(id = roomBlockID)
        roomFloorID = request.POST.get('floor_id')
        fetchedFloor = Floor.objects.get(id = roomFloorID)
        roomType = request.POST.get('room_type')
        roomCapacity = request.POST.get('capacity')
        try:
            Room.objects.create(name=roomName,
                                block=fetchedBlock,
                                floor=fetchedFloor,
                                type=roomType,
                                capacity=roomCapacity)
        except Exception as e:
            messages.info(request, e)
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_room(request, room_id):
    room = Room.objects.get(id = room_id)
    room.delete()
    return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def bulk_upload_academic_info_save(request):
    if request.method == 'POST':
        paramFile = io.TextIOWrapper(request.FILES['academic_file'].file)
        data = pd.read_csv(paramFile)

        for index, row in data.iterrows():
            if Block.objects.filter(name = str(row['Block Name'])).exists() is False:
                blockObj = Block.objects.create(
                    name = row['Block Name'],
                    block_desc = row['Block Desc'],
                )
            else:
                blockObj = Block.objects.filter(name = str(row['Block Name']))[0]
            
            if Floor.objects.filter(floor_name = str(row['Floor']), block__name = str(row['Block Name'])).exists() is False:
                floorObj = Floor.objects.create(
                    floor_name = row['Floor'],
                    block = blockObj,
                )
            else:
                floorObj = Floor.objects.filter(floor_name = str(row['Floor']))[0]
            
            if Room.objects.filter(block__name = str(row['Block Name']), floor__floor_name = str(row['Floor']), room_name = str(row['Room'])).exists() is False:
                Room.objects.create(
                    room_name = row['Room'],
                    block = blockObj,
                    floor = floorObj,
                    type = row['Room Type'],
                    capacity = row['Room Capacity'],
                )
            messages.success(request, "Bulk Import done")
        return redirect('manage_academic')

# Testing MTM
from .models import (Testing)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def manage_academic(request):
    blocks = Block.objects.all().order_by('name')
    floors = Floor.objects.all()
    rooms = Room.objects.all()
    roomTypeForm = RoomTypeForm()
    # Testing MTM
    test = Testing.objects.all()
    context = {
        "blocks": blocks,
        "floors": floors,
        "rooms": rooms,
        "roomTypeForm":roomTypeForm,
        "test":test,
    }
    return render(request, 'academic/academic.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def academic_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=academic_info_record' + \
        str(pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Block Name', 'Block Desc', 'Floor', 'Room', 
                    'Room Type', 'Room Capacity'])

    rooms = Room.objects.all()

    for i in rooms:
        writer.writerow([i.block.name, i.block.block_desc, i.floor.floor_name,
                        i.room_name, i.type, i.capacity])
    return response

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def sample_academic_info_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sample_academic_info_file' + \
        str(pydt.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Block Name', 'Block Desc', 'Floor', 'Room', 
                    'Room Type', 'Room Capacity'])

    rooms = Room.objects.all()

    for i in rooms:
        writer.writerow([i.block.name, i.block.block_desc, i.floor.floor_name,
                        i.room_name, i.type, i.capacity])
    return response

# Testing Many-to-Many

# Testing.objects.all().delete()

def TestingMet(request):
    if request.method == "POST":
        getName = request.POST['name']
        getMembers = request.POST.getlist('members')
        createObj = Testing.objects.create(name = getName)
        for i in getMembers:
            ithObj = Block.objects.get(id=i)
            createObj.members.add(ithObj)
    return redirect('manage_academic')