import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string

from django import http

import datetime as pydt
import httpagentparser
import re

from akira_apps.authentication.models import User_IP_B_List, UserLoginDetails

def verify_recaptcha(request):
    if request.method == "POST" and request.path != "/":
        recaptcha_response = request.POST.get('g-recaptcha-response')
        user_agent = request.META['HTTP_USER_AGENT']
        browser = httpagentparser.detect(user_agent)
        if not browser:
            browser = user_agent.split('/')[0]
        else:
            browser = browser['browser']['name']

        res = re.findall(r'\(.*?\)', user_agent)
        OS_Details = res[0][1:-1]
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            spam_user_ip_address = x_forwarded_for.split(',')[0]
        else:
            spam_user_ip_address = request.META.get('REMOTE_ADDR')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success'] and \
                float(result['score']) > settings.RECAPTCHA_REQUIRED_SCORE:
            return None
        elif result['success'] == False:
            print(False)
            sld = UserLoginDetails(user_ip_address=spam_user_ip_address, os_details=OS_Details, browser_details=browser, attempt="Failed")
            sld.save()
            print(spam_user_ip_address)
            twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
            check_failed_login_attempts = UserLoginDetails.objects.filter(user_ip_address = spam_user_ip_address, attempt="Failed", created_at__gte=twenty_four_hrs).count()
            print(check_failed_login_attempts)
            if check_failed_login_attempts > 5:
                block_ip = User_IP_B_List(black_list=spam_user_ip_address)
                block_ip.save()
            BLOCKED_IPS = []
            get_black_list_ip = User_IP_B_List.objects.all()
            for i in get_black_list_ip:
                BLOCKED_IPS.append(i.black_list)
            print(BLOCKED_IPS)
            if spam_user_ip_address in BLOCKED_IPS:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        respond = render_to_string('G_Recaptcha/ReCaptcha_error.html')
        return HttpResponseBadRequest(respond)