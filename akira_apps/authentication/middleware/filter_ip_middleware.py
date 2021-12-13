from django import http

from akira_apps.authentication.models import User_IP_B_List

class FilterIPMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        BLOCKED_IPS = []
        get_ip_addr_black_list = User_IP_B_List.objects.all()
        for i in get_ip_addr_black_list:
            BLOCKED_IPS.append(i.black_list)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        if ip in BLOCKED_IPS:
            return http.HttpResponseForbidden('IP Blocked')

        return self.get_response(request)