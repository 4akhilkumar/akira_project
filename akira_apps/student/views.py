from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from akira_apps.authentication.models import UserLoginDetails

@login_required
def student_dashboard(request):
    previous_user_login_details = UserLoginDetails.objects.filter(user__username = request.user)
    context = {
        "previous_user_login_details":previous_user_login_details,
    }
    return render(request, 'student/dashboard.html', context)