from django.shortcuts import redirect, render
from .models import (Resource)

def manage_resources(request):
    all_resources = Resource.objects.all()
    context = {
        "all_resources":all_resources,
    }
    return render(request, 'shigen/manage_resources.html', context)

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