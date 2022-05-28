from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

import datetime as pydt
import base64
import json
import requests
import re
import httpagentparser
import random
import string

from akira_apps.URLShortener.models import (URLShortenerMC, ShortenURLStat)

def randomString():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def getOS_Browser_info(request):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']
    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]
    return [browser, OS_Details]

def isLongURLSafe(request, long_url):
    in_url = long_url
    if not re.match(r'^https?://', in_url):
        in_url = 'http://' + in_url
    
    try:
        base64URL = base64.urlsafe_b64encode(in_url.encode()).decode().strip("=")
        url = "https://www.virustotal.com/api/v3/urls/%s" % (base64URL)
        headers = {
            "Accept": "application/json",
            "x-apikey": settings.VIRUS_TOTAL_API_KEY
        }

        response = requests.request("GET", url, headers=headers)
        response_json = json.loads(response.text)
        malicious_count = response_json['data']['attributes']['last_analysis_stats']['malicious']
        suspicious_count = response_json['data']['attributes']['last_analysis_stats']['suspicious']

        if malicious_count > 0 or suspicious_count > 0:
            return False
        else:
            return True
    except Exception:
        return True

def shortenURL(request, short_url):
    if URLShortenerMC.objects.filter(long_url_path=short_url).exists() is True:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddr = x_forwarded_for.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            userObj = request.user
        else:
            userObj = None
        shortenerURL = URLShortenerMC.objects.get(long_url_path=short_url)
        ShortenURLStat.objects.create(
                                shortenURL=shortenerURL,
                                user = userObj,
                                user_ip_address=ipaddr,
                                os_details = getOS_Browser_info(request)[1],
                                browser_details = getOS_Browser_info(request)[0])
        if shortenerURL.expire_date_time is not None:
            if shortenerURL.expire_date_time < pydt.datetime.now():
                messages.error(request, "Shortened URL is expired.")
                return redirect('login')
        return HttpResponseRedirect(shortenerURL.long_url)
    else:
        messages.error(request, "Shortened URL is not exists.")
        return redirect('login')

@login_required(login_url=settings.LOGIN_URL)
def createShortURLAjax(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddr = x_forwarded_for.split(',')[0]
    else:
        ipaddr = request.META.get('REMOTE_ADDR')

    protocol = 'https' if request.is_secure() else 'http'
    domain_name = get_current_site(request).domain
    shorterner_url_prefix = protocol + '://' + domain_name + '/ak/'

    if request.method == "POST":
        userObj = request.user or None
        try:
            userBFP_ID = request.COOKIES['U53R_876_10']
        except Exception:
            userBFP_ID = None
        long_url = request.POST.get('long_url')
        if not re.match(r'^https?://', long_url):
            long_url = 'http://' + long_url
        customlink = request.POST.get('customize_path')
        if customlink is None or customlink == '':
            customlink = randomString()
        expire_status = request.POST.get('expire_status')
        if not expire_status == "on":
            expiredate = request.POST.get('expire_date')
            expiretime = request.POST.get('expire_time')
            if re.match(r'^\d{4}-\d{2}-\d{2}$', expiredate) and re.match("^[0-9]{2}:[0-9]{2}$", expiretime):
                print("Date and Time are in proper format")

                # Check Today's date
                if expiredate == pydt.date.today().strftime("%Y-%m-%d"):
                    # Checking given time is greater than current time or not
                    if expiretime > pydt.datetime.now().strftime("%H:%M:%S"):
                        expiredatetime = expiredate + " " + expiretime
                    else:
                        message = "Expire time is less than current time."
                        status = "error"
                        return JsonResponse({
                                'message':message,
                                'status':status
                            })
                
                # Checking yesterday's
                elif expiredate < pydt.date.today().strftime("%Y-%m-%d"):
                    message = "Expire date is less than current date."
                    status = "error"
                    return JsonResponse({
                            'message':message,
                            'status':status
                        })
                
                # Checking tomorrow's
                elif expiredate > pydt.date.today().strftime("%Y-%m-%d"):
                    if re.match("^[0-9]{2}:[0-9]{2}$", expiretime):
                        expiredatetime = expiredate + " " + expiretime
                    else:
                        message = "Enter proper expire time"
                        status = "error"
                        return JsonResponse({'status': status, 'message': message})
            else:
                message = "Enter proper time format"
                status = "error"
                return JsonResponse({'status': status, 'message': message})
        else:
            expiredatetime = None
        if URLShortenerMC.objects.filter(long_url_path=customlink).exists() is False:
            if re.match("^[a-zA-Z0-9]*$", customlink):
                if isLongURLSafe(request, long_url) is True:
                    gen_short_url = str(customlink)
                    shortenerURL = URLShortenerMC.objects.create(user=userObj,
                                                ip_addr = ipaddr, bfp_id = userBFP_ID,
                                                long_url=long_url, long_url_path = gen_short_url,
                                                expire_date_time = expiredatetime)
                    shorterner_url = shorterner_url_prefix + shortenerURL.long_url_path
                    
                    message = "URL Shortened Successfully"
                    status = "success"
                    return JsonResponse({'status': status, 'message': message, 'shortened_url': shorterner_url})
                else:
                    message = 'URL is not safe to be shortened'
                    status = "error"
                    return JsonResponse({'status': status, 'message': message})
            else:
                message = "Custom path can only contain alphanumeric characters."
                return JsonResponse({'status': status, 'message': message})
        else:
            message = "Path is already exists. Please choose simple unique Path."
            status = "error"
            return JsonResponse({'status': status, 'message': message})

@login_required(login_url=settings.LOGIN_URL)
def urlshortenermf(request):
    currentUser = request.user
    shorturls = URLShortenerMC.objects.filter(user=currentUser)
    activesu = URLShortenerMC.objects.filter(user=currentUser, expire_date_time__isnull=False)
    abouttoexpiresu = URLShortenerMC.objects.filter(user=currentUser, expire_date_time__gt = pydt.datetime.now())
    context = {
        'shorturls': shorturls,
        'activesu': activesu,
        'abouttoexpiresu': abouttoexpiresu
    }
    return render(request, 'URLShortener/shortURL.html', context)

@login_required(login_url=settings.LOGIN_URL)
def selectedSULogsAjax(request):
    if request.method == "POST":
        selectedSU_ID = request.POST.get('selected_su_id')
        selectedSU_Obj = URLShortenerMC.objects.get(id=selectedSU_ID, user = request.user)
        su_logs = ShortenURLStat.objects.filter(shortenURL = selectedSU_Obj)
        dict = {}
        for each in su_logs:
            dict[str(each.id)] = {
                'user_ip_address': each.user_ip_address,
                'os_details': each.os_details,
                'browser_details': each.browser_details,
                'visited_at': each.visited_at,
            }
        return JsonResponse(dict)