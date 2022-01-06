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
            currentPageURL = str(request.build_absolute_uri())
            # if not any(item in currentPageURL for item in DONT_SAVE_LIST):
            if ("SwitchDevice" or "admin" or "/") in currentPageURL:
                pass
            else:
                print(currentPageURL)
                UserPageVisits.objects.create(user=request.user, currentPage=currentPageURL)
                pass

        return self.get_response(request)