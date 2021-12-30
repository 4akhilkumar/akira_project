from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import datetime as pydt

from .models import (Resource)
from akira_apps.super_admin.decorators import allowed_users

@login_required(login_url=settings.LOGIN_URL)
def manage_resources(request):
    all_resources = Resource.objects.all()
    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
    new_resource = Resource.objects.filter(created_at__gte=twenty_four_hrs).count()
    context = {
        "all_resources":all_resources,
        "new_resource":new_resource,
    }
    return render(request, 'shigen/manage_resources.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def create_resource_save(request):
    if request.method == "POST":
        Name = request.POST.get("name")
        Thumbnail = request.FILES.get("thumbnail")
        Description = request.POST.get("description")
        videoFile = request.FILES.get("video_file")
        referenceInfo = request.POST.get("reference_info")
        hashTags = request.POST.get("hash_tags")
        try:
            Resource.objects.create(user = request.user,
                                name = Name,
                                thumbnail = Thumbnail,
                                description = Description,
                                video_file = videoFile,
                                reference_info = referenceInfo, 
                                hash_tags = hashTags)
        except Exception as e:
            print(e)
        return redirect('manage_resources')
    else:
        return redirect('manage_resources')

def view_resource(request, resource_id):
    get_resource = Resource.objects.get(id = resource_id)
    context = {
        "fetched_resource":get_resource,
    }
    return render(request, 'shigen/view_resource.html', context)

@allowed_users(allowed_roles=['Administrator', 'Head of the Department'])
def delete_resource(request, resource_id):
    get_resource = Resource.objects.get(id = resource_id)
    get_resource.delete()
    return redirect('manage_resources')