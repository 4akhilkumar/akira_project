from django.shortcuts import redirect, render
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse

import pandas as pd
import io
import csv
import datetime as pydt

from akira_apps.super_admin.decorators import allowed_users
from .models import (Block, Floor, Room)
from akira_apps.academic.forms import (RoomTypeForm)

def manage_academic(request):
    blocks = Block.objects.all().order_by('name')
    floors = Floor.objects.all()
    rooms = Room.objects.all()
    roomTypeForm = RoomTypeForm()
    context = {
        "blocks": blocks,
        "floors": floors,
        "rooms": rooms,
        "roomTypeForm":roomTypeForm,
    }
    return render(request, 'academic/academic.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_block(request):
    if request.method == 'POST':
        blockName = request.POST.get('name')
        blockDesc = request.POST.get('desc')
        try:
            Block.objects.create(name=blockName, desc=blockDesc)
        except Exception as e:
            messages.info(request, e)
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
            messages.info(request, e)
        return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_floor(request, floor_id):
    floor = Floor.objects.get(id = floor_id)
    floor.delete()
    return redirect('manage_academic')

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
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
            try:
                if Block.objects.filter(name = str(row['Block Name'])).exists() is False:
                    blockObj = Block.objects.create(
                        name = row['Block Name'],
                        desc = row['Block Desc'],
                    )
                else:
                    blockObj = Block.objects.filter(name = str(row['Block Name']))[0]
                
                if Floor.objects.filter(name = str(row['Floor']), block__name = str(row['Block Name'])).exists() is False:
                    floorObj = Floor.objects.create(
                        name = row['Floor'],
                        block = blockObj,
                    )
                else:
                    floorObj = Floor.objects.filter(name = str(row['Floor']))[0]
                
                if Room.objects.filter(block__name = str(row['Block Name']), floor__name = str(row['Floor']), name = str(row['Room'])).exists() is False:
                    Room.objects.create(
                        name = row['Room'],
                        block = blockObj,
                        floor = floorObj,
                        type = row['Room Type'],
                        capacity = row['Room Capacity'],
                    )
                messages.success(request, "Bulk Import done")
            except Exception as e:
                messages.error(request, e)
        return redirect('manage_academic')

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
        writer.writerow([i.block.name, i.block.desc, i.floor.name,
                        i.name, i.type, i.capacity])
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
        writer.writerow([i.block.name, i.block.desc, i.floor.floor_name,
                        i.room_name, i.type, i.capacity])
    return response