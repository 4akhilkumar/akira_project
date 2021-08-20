from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . models import UserLoginDetails

import datetime as pydt
import socket
import re
import httpagentparser

def user_login(request):
    current_time = pydt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = ""
    success_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_ip_address = request.POST.get('user_ip_address')

        if len(user_ip_address) > 0:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                success_message = "Login Successfull"

                save_login_details(request, username, user_ip_address)
                verify_login(request, username, current_time)

                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                if group == 'Student':
                    if (request.GET.get('next')):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('student_dashboard')
                elif group == 'Faculty':
                    if (request.GET.get('next')):
                        return redirect(request.GET.get('next'))
                    else: 
                        return redirect('faculty_dashboard')
                else:
                    if (request.GET.get('next')):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('super_admin_dashboard')
            else:
                error_message = "Username or Password is Incorrect!"
        else:
            error_message = "Check Your Internet Connection!"
    context = {
        "error_message":error_message,
        "success_message":success_message,
    }
    return render(request, 'authentication/login.html', context)

def save_login_details(request, user_name, user_ip_address):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]
    uid = User.objects.get(username=user_name)

    try:
        sld = UserLoginDetails(user_ip_address=user_ip_address, user=uid, os_details=OS_Details, browser_details=browser)
        sld.save()
    except Exception as e:
        return e

def verify_login(request, uid, current_time):
    current_uld = UserLoginDetails.objects.filter(user__username = uid)
    last_current_uld = UserLoginDetails.objects.filter(user__username = uid).order_by('-created_at')

    list_current_uld_ipa = []
    list_current_uld_osd = []
    list_current_uld_bd = []

    for i in range(len(current_uld)-1):
        list_current_uld_ipa.append(current_uld[i].user_ip_address)
        list_current_uld_osd.append(current_uld[i].os_details)
        list_current_uld_bd.append(current_uld[i].browser_details)

    user_ip_address = list(last_current_uld)[0].user_ip_address
    os_details = list(last_current_uld)[0].os_details
    browser_details = list(last_current_uld)[0].browser_details

    for i in range(len(current_uld)-1):
        count = 0
        if user_ip_address in list_current_uld_ipa:
            count += 1
        if os_details in list_current_uld_osd:
            count += 1
        if browser_details in list_current_uld_bd:
            count += 1
        if(count<3):
            context = {
                "first_name":request.user.first_name,
                "email":request.user.email,
                "user_ip_address":user_ip_address,
                "os_details":os_details,
                "browser_details":browser_details,
                "current_time":current_time,
            }
            template = render_to_string('authentication/login_alert_email.html', context)
            try:
                # print("Mail Sent!") 
                send_mail('Akira Account Login Alert', template, settings.EMAIL_HOST_USER, [request.user.email], html_message=template)
            except Exception as e:
                print(e)
            break
    return "Okay"

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    current_time = pydt.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z %z")
    # return render(request, 'authentication/dashboard.html')
    return HttpResponse(current_time)