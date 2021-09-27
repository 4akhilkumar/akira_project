from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from akira_apps.authentication.models import UserLoginDetails

import secrets

@login_required
def student_dashboard(request):
    previous_user_login_details = UserLoginDetails.objects.filter(user__username = request.user)
    rAnd0m123 = secrets.token_urlsafe(16)
    context = {
        "previous_user_login_details":previous_user_login_details,
        "rAnd0m123":rAnd0m123,
    }
    return render(request, 'student/dashboard.html', context)