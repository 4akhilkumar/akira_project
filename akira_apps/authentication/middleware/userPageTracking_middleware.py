from akira_apps.authentication.models import UserPageVisits

class userPageTrackingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        if request.user.is_authenticated:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            currentPageURL = str(request.build_absolute_uri())

            DONT_SAVE_LIST = ["Device", "admin", "logout", "media", "static"]
            if any(ext in currentPageURL for ext in DONT_SAVE_LIST):
                pass
            else:
                if UserPageVisits.objects.filter(user=request.user, currentPage=currentPageURL, userIPAddr=ip).exists() is True:
                    UserPageVisits.objects.filter(user=request.user, currentPage=currentPageURL, userIPAddr=ip).delete()
                    UserPageVisits.objects.create(user=request.user, currentPage=currentPageURL, userIPAddr=ip)
                else:
                    UserPageVisits.objects.create(user=request.user, currentPage=currentPageURL, userIPAddr=ip)

        return self.get_response(request)