from django import http

import datetime as pydt

from akira_apps.authentication.models import (User_IP_B_List, User_IP_S_List, UserLoginDetails, User_BackUp_Codes_Login_Attempts)

class FilterIPMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
        ULDFCNS = UserLoginDetails.objects.filter(user_ip_address = ip, attempt = "Failed", reason = "Connection is NOT secured", created_at__gte=twenty_four_hrs).count()
        UBCLAF = User_BackUp_Codes_Login_Attempts.objects.filter(userIPAddr = ip, status = "Failed", created_at__gte=twenty_four_hrs).count()
        if User_IP_B_List.objects.filter(black_list = ip).exists() is True:
            return http.HttpResponseForbidden('IP Blocked')
        elif (ULDFCNS < 1) and (UBCLAF < 1):
            User_IP_S_List.objects.filter(suspicious_list = ip).delete()

        return self.get_response(request)