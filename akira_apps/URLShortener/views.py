from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect

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
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

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

def shortURL(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddr = x_forwarded_for.split(',')[0]
    else:
        ipaddr = request.META.get('REMOTE_ADDR')

    getShortedURLs = URLShortenerMC.objects.filter(ip_addr=ipaddr)
    protocol = 'https' if request.is_secure() else 'http'
    domain_name = get_current_site(request).domain
    shorterner_url_prefix = protocol + '://' + domain_name + '/akira/'

    if request.method == "POST":
        if request.user.is_authenticated:
            userObj = request.user
        else:
            userObj = None

        userBFP_ID, expiretime, expiredate = None, None, None
        userBFP_ID = request.POST.get('fingerprint')

        long_url = request.POST.get('long_url').strip()
        if not re.match(r'^https?://', long_url):
            long_url = 'http://' + long_url
        customlink = request.POST.get('long_url_alias').strip()
        expire_status = request.POST.get('expire_status')
        if not expire_status == "on":
            expiredate = request.POST.get('expire_date')
            expiretime = request.POST.get('expire_time')
            expiretimedate = expiredate + " " + expiretime
        else:
            expiretimedate = None

        if customlink is None or customlink == '':
            customlink = randomString()
        if URLShortenerMC.objects.filter(short_url=customlink).exists() is False:
            if re.match("^[a-zA-Z0-9]*$", customlink):
                if isLongURLSafe(request, long_url) is True:
                    gen_short_url = str(customlink) 
                    if userObj:
                        shortenerURL = URLShortenerMC.objects.create(user=userObj,
                                                    ip_addr = ipaddr, bfp = userBFP_ID,
                                                    long_url=long_url, short_url = gen_short_url,
                                                    expire_time_date = expiretimedate)
                    else:
                        shortenerURL = URLShortenerMC.objects.create(user=userObj,
                                                    ip_addr = ipaddr, bfp = userBFP_ID,
                                                    long_url=long_url, short_url = gen_short_url,
                                                    expire_time_date = expiretimedate)
                    messages.success(request, 'URL Shortened Successfully')
                    shorterner_url = shorterner_url_prefix + shortenerURL.short_url
                    context = {
                        'shorterner_url': shorterner_url,
                    }
                    return render(request, 'URLShortener/shortURL.html', context)
                else:
                    messages.error(request, 'URL is not safe to be shortened')
            else:
                messages.error(request, "Custom link can only contain alphanumeric characters.")
        else:
            messages.error(request, "Alias is already exists.")
            messages.info(request, "Please choose simple unique alias.")
        return redirect('shortURL')
    context = {
        'getShortedURLs': getShortedURLs,
        'shorterner_url_prefix': shorterner_url_prefix,
        'protocol_current_domain': protocol + '://' + domain_name,
    }
    return render(request, 'URLShortener/shortURL.html', context)

def shortenURL(request, short_url):
    if URLShortenerMC.objects.filter(short_url=short_url).exists() is True:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddr = x_forwarded_for.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            userObj = request.user
        else:
            userObj = None
        shortenerURL = URLShortenerMC.objects.get(short_url=short_url)
        ShortenURLStat.objects.create(
                                shortenURL=shortenerURL,
                                user = userObj,
                                user_ip_address=ipaddr,
                                os_details = getOS_Browser_info(request)[1],
                                browser_details = getOS_Browser_info(request)[0])
        if shortenerURL.expire_time_date is not None:
            if shortenerURL.expire_time_date < pydt.datetime.now():
                messages.error(request, "This URL is expired.")
                return redirect('shortURL')
        return HttpResponseRedirect(shortenerURL.long_url)
    else:
        messages.error(request, "URL is not exists.")
        return redirect('shortURL')