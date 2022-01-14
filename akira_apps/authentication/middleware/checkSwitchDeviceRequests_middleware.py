from akira_apps.authentication.models import SwitchDevice

import datetime as pydt

class checkSwitchDeviceRequestsMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        
        thirty_minutes_ago = pydt.datetime.now() + pydt.timedelta(minutes=-30)
        if SwitchDevice.objects.filter(userConfirm = "Pending", created_at__gte = thirty_minutes_ago).exists() is True:
            SwitchDevice.objects.filter(userConfirm = "Pending", created_at__gte = thirty_minutes_ago).count()

        return self.get_response(request)