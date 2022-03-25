import datetime as pydt

from akira_apps.authentication.models import (UserLoginDetails)
from akira_apps.authentication.views import (UsernameEncryptedCookie, DecryptEncryptedCookie)

class userDeviceCookieMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization, when the webserver starts.
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                getDeviceCCookieObj = UserLoginDetails.objects.get(user = request.user, sessionKey = request.session.session_key)
            except Exception:
                getDeviceCCookieObj = None
            
            ranKey = UsernameEncryptedCookie(request, request.user.username)
            cookie_max_age = 1209600
            expire_time = pydt.datetime.strftime(pydt.datetime.utcnow() + pydt.timedelta(seconds=cookie_max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
            
            if getDeviceCCookieObj is not None and getDeviceCCookieObj.Logoutcookie is None:

                try:
                    getEncryptedCookie = request.COOKIES['access_token']
                except Exception:
                    getEncryptedCookie = None
                try:
                    getEncryptedGuestCookie = request.COOKIES['guest_token']
                except Exception:
                    getEncryptedGuestCookie = None
                
                if getEncryptedCookie and getEncryptedGuestCookie:
                    print("1. Both cookies present")
                    if UserLoginDetails.objects.filter(user = request.user, Logoutcookie = getEncryptedCookie).last() is not None:
                        print("2. This Access Cookie is belongs to first user")
                        # Create new cookie and set it in client side and save it in database
                        response.set_cookie(key='access_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                        getDeviceCCookieObj.Logoutcookie = ranKey
                        getDeviceCCookieObj.save()
                    elif UserLoginDetails.objects.filter(user = request.user, Logoutcookie = getEncryptedGuestCookie).last() is not None:
                        print("3. This Guest Cookie is belongs to second user")
                        # Create new Guest Cookie and set it in client side and save it in database
                        response.set_cookie(key='guest_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                        getDeviceCCookieObj.Logoutcookie = ranKey
                        getDeviceCCookieObj.save()
                    else:
                        print("4. Third User")
                        # Replace the guest cookie with new value related to the third user
                        response.set_cookie(key='guest_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                        getDeviceCCookieObj.Logoutcookie = ranKey
                        getDeviceCCookieObj.save()
                        print("Here1")
                        return response

                elif getEncryptedCookie:
                    print("5. Only access_token cookie present")
                    if DecryptEncryptedCookie(request, request.user.username, getEncryptedCookie) is True:
                    # if UserLoginDetails.objects.filter(user = request.user, Logoutcookie = getEncryptedCookie).last() is not None:
                        print("6. This Access Cookie is belongs to first user")
                        # Create new cookie and set it in client side and save it in database
                        response.set_cookie(key='access_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                        getDeviceCCookieObj.Logoutcookie = ranKey
                        getDeviceCCookieObj.save()
                    else:
                        print("7. Access Cookie does not belongs to first user")
                        # Create Guest Cookie
                        response.set_cookie(key='guest_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                        getDeviceCCookieObj.Logoutcookie = ranKey
                        getDeviceCCookieObj.save()
                        print("Here2")
                        return response
                else:
                    print("8. No cookie present")
                    # Create access_token cookie
                    response.set_cookie(key='access_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
                    getDeviceCCookieObj.Logoutcookie = ranKey
                    getDeviceCCookieObj.save()
                    return response
        return response