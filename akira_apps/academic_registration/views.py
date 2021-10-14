from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from akira_apps.academic_registration.forms import SemesterForm

from akira_apps.academic_registration.models import Semester

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