from django.shortcuts import render

# Create your views here.
def academic_registration_dashboard(request):
    context = {
        
    }
    return render(request, 'academic_registration/dashboard.html', context)