from django import http
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

class isAdminExistMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        
        # print(request.get_full_path())
        currentPageURL = str(request.build_absolute_uri())

        WHITELISTURL = ["adminInstituteRegistration", "confirm_admin_email"]

        if not User.objects.filter(groups__name='Administrator').exists():
            if any(ext in currentPageURL for ext in WHITELISTURL):
                pass
            else:
                messages.info(request, "In order to utilize the AkirA Application, please create an Admininstrator account.")
                return redirect('/super_admin/adminInstituteRegistration/')

        return self.get_response(request)