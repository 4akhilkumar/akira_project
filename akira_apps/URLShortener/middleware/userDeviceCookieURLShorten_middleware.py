import datetime as pydt

class userDeviceCookieURLShortenMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)
        
        ranKey = ''
        cookie_max_age = 1209600
        expire_time = pydt.datetime.strftime(pydt.datetime.utcnow() + pydt.timedelta(seconds=cookie_max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

        try:
            getEncryptedCookie = request.COOKIES['access_token']
        except Exception:
            getEncryptedCookie = None
            response.set_cookie(key='access_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
            return response
        return response