from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.core import mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import http
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages

from akira_apps.authentication.token import account_activation_token

from django.contrib.auth import get_user_model

import datetime as pydt
import socket
import re
import httpagentparser
import json
import requests

from akira_apps.super_admin.decorators import unauthenticated_user, allowed_users

from . models import UserLoginDetails, User_IP_B_List

from akira_apps.staff.urls import *
from akira_apps.super_admin.urls import *
from akira_apps.academic_registration.urls import *

@unauthenticated_user
def user_login(request):
    BLOCKED_IPS = []
    get_black_list_ip = User_IP_B_List.objects.all()
    for i in get_black_list_ip:
        BLOCKED_IPS.append(i.black_list)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip in BLOCKED_IPS:
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    else:
        current_time = pydt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if request.method == 'POST':
            username = request.POST.get('username')

            ASCII_Username = []
            for i in range(len(username)):
                ASCII_Username.append(ord(username[i]))
            ASCII_Username_Sum = sum(ASCII_Username)

            encrypted_username = ""
            for i in range(len(username)):
                encrypted_username += chr(ord(username[i]) + ASCII_Username_Sum)

            encrypted_password = request.POST.get('encrypted_password')

            password = ""
            de_key_length = len(encrypted_password) - len(username)
            for i in range(de_key_length):
                password += chr(ord(encrypted_password[i]) - ASCII_Username_Sum)

            user_ip_address = ip

            captcha_token=request.POST.get("g-recaptcha-response")
            cap_url="https://www.google.com/recaptcha/api/siteverify"
            cap_secret="6LfmDxMdAAAAAI9NEfnM3BUqHfF-zAMLLJOwSRw8"
            cap_data={"secret":cap_secret,"response":captcha_token}
            cap_server_response=requests.post(url=cap_url,data=cap_data)
            cap_json=json.loads(cap_server_response.text)

            existing_user_records = User.objects.all()
            list_existing_user_records = []
            for i in existing_user_records:
                list_existing_user_records.append(i.username)
            
            if cap_json['success']==True:
                if username in list_existing_user_records:
                    user = User.objects.get(username = username)
                    if user.is_active == True:
                        if encrypted_username in encrypted_password:
                            user = authenticate(request, username=username, password=password)
                            
                            if user is not None:
                                login(request, user)
                                save_login_details(request, username, user_ip_address, "Success")
                                length_UserLoginDetails = UserLoginDetails.objects.all().count()
                                if length_UserLoginDetails > 2:
                                    verify_login(request, username, current_time)

                                group = None
                                if request.user.groups.exists():
                                    group = request.user.groups.all()[0].name
                                if group == 'Student':
                                    if (request.GET.get('next')):
                                        return redirect(request.GET.get('next'))
                                    else:
                                        return redirect('student_dashboard')
                                elif group == 'Staff':
                                    if (request.GET.get('next')):
                                        return redirect(request.GET.get('next'))
                                    else: 
                                        return redirect('staff_dashboard')
                                elif group == 'Head of the Department':
                                    if (request.GET.get('next')):
                                        return redirect(request.GET.get('next'))
                                    else: 
                                        return redirect('hod_dashboard')
                                elif group == 'Course Co-Ordinator':
                                    if (request.GET.get('next')):
                                        return redirect(request.GET.get('next'))
                                    else: 
                                        return redirect('cc_dashboard')
                                elif group == 'Administrator':
                                    if (request.GET.get('next')):
                                        return redirect(request.GET.get('next'))
                                    else:
                                        return redirect('super_admin_dashboard')
                            else:
                                messages.warning(request, 'Username or Password is Incorrect!')
                                list_users = User.objects.all()
                                LIST_USERS = []
                                for i in list_users:
                                    LIST_USERS.append(i.username)
                                if username in LIST_USERS or cap_json['success']==False:
                                    save_login_details(request, username, user_ip_address, "Failed")
                                    detect_spam_login(request, username, user_ip_address)
                                return redirect('login')
                        else:
                            messages.error(request, 'Connection is NOT secured!')
                            return redirect('login')
                    else:
                        messages.info(request, 'You account has been disabled temporarily')
                        return redirect('login')
                else:
                    messages.error(request, 'No such account exist!')
                    if username in list_existing_user_records:
                        save_login_details(request, username, user_ip_address, "Failed")
                        detect_spam_login(request, username, user_ip_address)
                    else:
                        save_login_details(request, None, user_ip_address, "Failed")
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid Captcha try again!')
                if username in list_existing_user_records:
                    save_login_details(request, username, user_ip_address, "Failed")
                    detect_spam_login(request, username, user_ip_address)
                else:
                    save_login_details(request, None, user_ip_address, "Failed")
                return redirect('login')
        return render(request, 'authentication/login.html')

def save_login_details(request, user_name, user_ip_address, attempt):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]
    if user_name == None:
        sld = UserLoginDetails(user_ip_address=user_ip_address, os_details=OS_Details, browser_details=browser, attempt=attempt)
        sld.save()
    else:
        uid = User.objects.get(username=user_name)
        try:
            sld = UserLoginDetails(user_ip_address=user_ip_address, user=uid, os_details=OS_Details, browser_details=browser, attempt=attempt)
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
        save_current_uld_status = UserLoginDetails.objects.get(id=last_current_uld[0].id)
        save_current_uld_status.status = count
        save_current_uld_status.save()
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
                send_mail('Akira Account Login Alert', template, settings.EMAIL_HOST_USER, [request.user.email], html_message=template)
            except Exception as e:
                messages.warning(request, e)
            break
    return "verify_login"

def detect_spam_login(request, uid, spam_user_ip_address):
    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
    check_failed_login_attempts = UserLoginDetails.objects.filter(user__username = uid, attempt="Failed", created_at__gte=twenty_four_hrs).count()
    if check_failed_login_attempts == 3:
        messages.info(request, 'It seems to be you have forgotten your password!')
        messages.info(request, 'So, Please reset your password')
        return redirect('login')
    elif check_failed_login_attempts > 4:
        user = User.objects.get(username = uid)
        block_ip = User_IP_B_List(black_list=spam_user_ip_address, login_user = user)
        block_ip.save()
        user.is_active = False
        user.save()
        current_site = get_current_site(request)  
        mail_subject = 'Re-Activate Your AkirA Account'
        message = render_to_string('authentication/acc_active_email.html', {
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        current_user = User.objects.get(username = uid)
        to_email = current_user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        messages.warning(request, "Please Check Your EMail Inbox")
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')

def activate(request, uidb64, token):
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for Re-Activating your account. Now you can login your account.')
    else:  
        return HttpResponse('Activation link is invalid!')

@login_required(login_url=settings.LOGIN_URL)
def logoutUser(request):
    logout(request)
    return redirect('login')

# lst = UserLoginDetails.objects.all()
# for i in lst:
#     delete_all_records = UserLoginDetails.objects.get(id=i.id)
#     delete_all_records.delete()

# lst = User_IP_B_List.objects.all()
# for i in lst:
#     delete_all_records = User_IP_B_List.objects.get(id=i.id)
#     delete_all_records.delete()

# user = User.objects.get(username = 'hari.vege')
# user.is_active = True  
# user.save()