from akira_apps.authentication.models import UserPageVisits

class userPageTrackingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        if request.user.is_authenticated:
            DONT_SAVE_LIST = [
                "SwitchDevice",
                "admin",
                "/"
            ]
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            currentPageURL = str(request.build_absolute_uri())
            # if not any(item in currentPageURL for item in DONT_SAVE_LIST):
            if ("Device" or "admin" or "/") in currentPageURL:
                pass
            else:
                print(currentPageURL)
                UserPageVisits.objects.create(user=request.user, currentPage=currentPageURL, userIPAddr=ip)
                pass

        return self.get_response(request)