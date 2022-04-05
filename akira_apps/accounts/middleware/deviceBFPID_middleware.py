from django import http
from django.http import HttpResponse

import datetime as pydt

class DeviceBFPIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            BFP_ID = str(request.headers.get('Browser-Fignerprint-ID'))
            cookie_max_age = 1209600
            expire_time = pydt.datetime.strftime(pydt.datetime.utcnow() + pydt.timedelta(seconds=cookie_max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie(key='U53R_876_10', value=str(BFP_ID), max_age=cookie_max_age, expires=expire_time)
            return response
        return response