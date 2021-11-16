from django.http.response import Http404, HttpResponse
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
from akira_apps.accounts.models import TwoFactorAuth

from akira_apps.authentication.token import account_activation_token

from django.contrib.auth import get_user_model

import datetime as pydt
import re
import httpagentparser
import json
import requests

from akira_apps.super_admin.decorators import unauthenticated_user, allowed_users

from . models import User_BackUp_Codes, User_BackUp_Codes_Login_Attempts, UserLoginDetails, User_IP_B_List, UserVerificationStatus

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

            try:
                status_2fa = TwoFactorAuth.objects.get(user__username=username)
            except TwoFactorAuth.DoesNotExist:
                status_2fa = None
            current_user_2fa_status = 0
            if (status_2fa != None) and (status_2fa.twofa == 0):
                current_user_2fa_status = 0
            elif (status_2fa != None) and (status_2fa.twofa == 1):
                current_user_2fa_status = 1
            else:
                current_user_2fa_status = 0

            ASCII_Username = []
            for i in range(len(username)):
                ASCII_Username.append(ord(username[i]))
            ASCII_Username_Sum = sum(ASCII_Username)

            encrypted_username = ""
            for i in range(len(username)):
                encrypted_username += chr(ord(username[i]) + ASCII_Username_Sum)

            custom_encrypted_username = ""
            for i in range(len(username)):
                custom_encrypted_username += chr(ord(username[i]) + 468)

            ep = request.POST.get('encrypted_password')

            List1 = list(ep)
            List2 = list(encrypted_username)
            check =  any(item in List1 for item in List2)

            l_rot = 0
            r_rot = len(username)
            temp = (l_rot - r_rot) % len(ep) 
            encrypted_password = ep[temp : ] + ep[ : temp]

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
                        if check is True:
                            user = authenticate(request, username=username, password=password)
                            if user is not None:
                                save_login_details(request, username, user_ip_address, "Not Confirmed Yet!")
                                length_UserLoginDetails = UserLoginDetails.objects.filter(user__username=username).count()
                                if length_UserLoginDetails > 6:
                                    verify_login(request, username, current_time, user)
                                
                                current_userverificationstatus_have_to_verify_count = UserVerificationStatus.objects.filter(user__username=username, status="Have to Verify").count()
                                current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=username, status="Have to Verify").order_by('-created_at')
                                if (current_user_2fa_status == 0) and ((not current_userverificationstatus) or (current_userverificationstatus_have_to_verify_count == 0) or (current_userverificationstatus[0].status == "Verified")):
                                    login(request, user)
                                    try:
                                        current_userlogindetailsObject = UserLoginDetails.objects.filter(user__username=username, attempt="Not Confirmed Yet!")
                                        current_userlogindetailsObject_count = UserLoginDetails.objects.filter(user__username=username, attempt="Not Confirmed Yet!").count()
                                    except UserLoginDetails.DoesNotExist:
                                        current_userlogindetailsObject = None
                                    if (current_userlogindetailsObject != None) and (current_userlogindetailsObject_count > 0):
                                        current_userlogindetailsObject = UserLoginDetails.objects.filter(user__username=username, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                                        get_current_userlogindetailsObject_Id = UserLoginDetails.objects.get(id=current_userlogindetailsObject.id)
                                        get_current_userlogindetailsObject_Id.attempt = "Success"
                                        get_current_userlogindetailsObject_Id.save()
                                    
                                    try:
                                        userverificationstatusObject = UserVerificationStatus.objects.get(user__username=username)
                                    except UserVerificationStatus.DoesNotExist:
                                        userverificationstatusObject = None
                                    if userverificationstatusObject != None:
                                        userverificationstatusObject = UserVerificationStatus.objects.filter(user__username=username, status=0).order_by('-created_at')[0]
                                        get_userverificationstatusObject_Id = UserVerificationStatus.objects.get(id=userverificationstatusObject.id)
                                        get_userverificationstatusObject_Id.status = "Verified"
                                        get_userverificationstatusObject_Id.save()
                                    
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
                                elif current_user_2fa_status == 1:
                                    user.is_active == False
                                    user.save()
                                    return redirect('twofa_verify_its_you', username=custom_encrypted_username)
                                else:
                                    return redirect('verify_its_you', username=custom_encrypted_username)
                            else:
                                messages.warning(request, 'Username or Password is Incorrect!')
                                list_users = User.objects.all()
                                LIST_USERS = []
                                for i in list_users:
                                    LIST_USERS.append(i.username)
                                if username in LIST_USERS:
                                    save_login_details(request, username, user_ip_address, "Failed")
                                    detect_spam_login(request, username, user_ip_address)
                                return redirect('login')
                        else:
                            messages.error(request, 'Connection is NOT secured!')
                            return redirect('login')
                    else:
                        messages.info(request, 'You account has been disabled temporarily')
                        return redirect('verify_its_you', username=custom_encrypted_username)
                else:
                    messages.error(request, 'No such account exist!')
                    if username in list_existing_user_records:
                        save_login_details(request, username, user_ip_address, "Failed")
                        detect_spam_login(request, username, user_ip_address)
                    else:
                        save_login_details(request, None, user_ip_address, "Failed")
                        detect_spam_login(request, None, user_ip_address)
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid Captcha try again!')
                if username in list_existing_user_records:
                    save_login_details(request, username, user_ip_address, "Failed")
                    detect_spam_login(request, username, user_ip_address)
                else:
                    save_login_details(request, None, user_ip_address, "Failed")
                    detect_spam_login(request, None, user_ip_address)
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

def verify_login(request, uid, current_time, user):
    current_uld = UserLoginDetails.objects.filter(user__username = uid)
    last_current_uld = UserLoginDetails.objects.filter(user__username = uid).order_by('-created_at')
    current_user = User.objects.get(username=uid)
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
            count += 8
        if os_details in list_current_uld_osd:
            count += 4
        if browser_details in list_current_uld_bd:
            count += 2
        save_current_uld_status = UserLoginDetails.objects.get(id=last_current_uld[0].id)
        save_current_uld_status.status = count
        save_current_uld_status.save()
        if(count>=4 and count<=12):
            login(request, user)
            try:
                userlogindetailsObject = UserLoginDetails.objects.get(user__username=user)
                userlogindetailsObject_count = UserLoginDetails.objects.filter(user__username=user, attempt="Not Confirmed Yet!").count()
            except UserLoginDetails.DoesNotExist:
                userlogindetailsObject = None
            if (userlogindetailsObject != None) and (userlogindetailsObject_count > 0):
                get_attempt_ncy = UserLoginDetails.objects.filter(user__username=user, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
                update_attempt_ncy.attempt = "Success"
                update_attempt_ncy.save()
            context = {
                "first_name":current_user.first_name,
                "email":current_user.email,
                "user_ip_address":user_ip_address,
                "os_details":os_details,
                "browser_details":browser_details,
                "current_time":current_time,
            }
            template = render_to_string('authentication/login_alert_email.html', context)
            try:
                send_mail('Akira Account Login Alert', template, settings.EMAIL_HOST_USER, [current_user.email], html_message=template)
            except Exception as e:
                messages.warning(request, e)
            break
        elif count<=2:
            user = User.objects.get(username = user.username)
            user.is_active = False
            user.save()
            userverificationstatus = UserVerificationStatus(user=user, status="Have to Verify")
            userverificationstatus.save()
            break
    return None

def verify_its_you(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)
    try:
        status_2fa = TwoFactorAuth.objects.get(user__username=custom_decrypted_username)
    except TwoFactorAuth.DoesNotExist:
        status_2fa = None
    current_user_2fa_status = 0
    if (status_2fa != None) and (status_2fa.twofa == 0):
        current_user_2fa_status = 0
    elif (status_2fa != None) and (status_2fa.twofa == 1):
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0
    try:
        uvs = UserVerificationStatus.objects.get(user__username=custom_decrypted_username)
    except UserVerificationStatus.DoesNotExist:
        uvs = None
    if uvs != None:
        current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).order_by('-created_at')[0]
    current_userverificationstatus_count = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).count()
    if (current_user_2fa_status == 0) and ((current_userverificationstatus_count == 0) or (current_userverificationstatus_count > 0 and current_userverificationstatus.status == "Verified")):
        return redirect('login')
    else:
        context = {
            "username":username,
        }
        return render(request, 'authentication/verify_its_you.html', context)

def verify_user_by_email(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)

    try:
        status_2fa = TwoFactorAuth.objects.get(user__username=custom_decrypted_username)
    except TwoFactorAuth.DoesNotExist:
        status_2fa = None
    current_user_2fa_status = 0
    if (status_2fa != None) and (status_2fa.twofa == 0):
        current_user_2fa_status = 0
    elif (status_2fa != None) and (status_2fa.twofa == 1):
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0
    current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).order_by('-created_at')[0]
    current_userverificationstatus_count = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).count()
    if (current_user_2fa_status == 0) and ((current_userverificationstatus_count == 0) or (current_userverificationstatus_count > 0 and current_userverificationstatus.status == "Verified")):
        return redirect('login')
    else:
        user = User.objects.get(username = custom_decrypted_username)
        current_site = get_current_site(request)
        mail_subject = "Verify It's You! - AkirA"
        message = render_to_string('authentication/user_confirmation_email.html', {
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        current_user = User.objects.get(username = custom_decrypted_username)
        to_email = current_user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        messages.warning(request, "Please Check Your EMail Inbox")
        return redirect('login')

def confirm(request, uidb64, token):
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True
        user.save()
        try:
            current_userverificationstatus = UserVerificationStatus.objects.filter(user=user, status="Have to Verify").order_by('-created_at')[0]
            userverificationstatus = UserVerificationStatus.objects.get(id=current_userverificationstatus.id)
            userverificationstatus.status="Verified"
            userverificationstatus.save()
            messages.success(request, "Thank you for confirming that's you.")
            return redirect('login')
        except Exception as e:
            messages.info(request, 'You have been confirmed already!')
            return redirect('login')
    else:  
        messages.warning(request, "Confirmation link is invalid!")
        return redirect('login')

def detect_spam_login(request, uid, spam_user_ip_address):
    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
    if uid == None:
        check_failed_login_attempts = UserLoginDetails.objects.filter(user_ip_address = spam_user_ip_address, attempt="Failed", created_at__gte=twenty_four_hrs).count()
        if check_failed_login_attempts > 4:
            block_ip = User_IP_B_List(black_list=spam_user_ip_address)
            block_ip.save()
    elif uid != None:
        check_failed_login_attempts = UserLoginDetails.objects.filter(user__username = uid, attempt="Failed", created_at__gte=twenty_four_hrs).count()
        if check_failed_login_attempts == 3:
            messages.info(request, 'It seems to be you have forgotten your password!')
            messages.info(request, 'So, Please reset your password')
            return redirect('login')
        elif check_failed_login_attempts > 5:
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
            messages.warning(request, "Please Check Your Email Inbox")
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

def verify_user_by_backup_codes(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)
    try:
        status_2fa = TwoFactorAuth.objects.get(user__username=custom_decrypted_username)
    except TwoFactorAuth.DoesNotExist:
        status_2fa = None
    current_user_2fa_status = 0
    if (status_2fa != None) and (status_2fa.twofa == 0):
        current_user_2fa_status = 0
    elif (status_2fa != None) and (status_2fa.twofa == 1):
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0
    try:
        uvs = UserVerificationStatus.objects.get(user__username=custom_decrypted_username)
    except UserVerificationStatus.DoesNotExist:
        uvs = None
    if uvs != None:
        current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).order_by('-created_at')[0]
    current_userverificationstatus_count = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).count()
    if (current_user_2fa_status == 0) and ((current_userverificationstatus_count == 0) or (current_userverificationstatus_count > 0 and current_userverificationstatus.status == "Verified")):
        return redirect('login')
    else:
        user = User.objects.get(username = custom_decrypted_username)
        if request.method == 'POST':
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            user_confirm = 0
            backup_code = request.POST.get('backup_code')
            current_user_backup_codes = User_BackUp_Codes.objects.get(user=user)
            backup_codes_with_hash = current_user_backup_codes.backup_codes
            splitup_backup_codes = backup_codes_with_hash.split('#')
            align_backup_code = []
            for i in splitup_backup_codes:
                align_backup_code.append(i)
            if backup_code in align_backup_code:
                user_confirm = 1
                align_backup_code.remove(backup_code)
                join_hash = '#'.join(align_backup_code)
                userbackupcodes = User_BackUp_Codes.objects.get(id=current_user_backup_codes.id)
                userbackupcodes.backup_codes = join_hash
                userbackupcodes.save()
                user = User.objects.get(username = user.username)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('login')
            else:
                user_confirm = 2
                update_attempt_failed = User_BackUp_Codes_Login_Attempts(user = user, attempt = user_confirm, status = "Failed")
                update_attempt_failed.save()
                backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(user = user, status = "Failed").count()
                if backup_code_attempt_status_count > 4:
                    block_ip = User_IP_B_List(black_list=ip)
                    block_ip.save()
                else:
                    return redirect('verify_user_by_backup_codes', username=username)
        else:
            return render(request, 'authentication/enter_backup_code.html')

def twofa_verify_its_you(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)
    
    user = User.objects.get(username=custom_decrypted_username)
    first_name = user.first_name
    context = {
        "username":user,
        "encrypted_username":username,
        "first_name":first_name,
    }
    return render(request, 'authentication/twofactorauth.html', context)

def twofa_verify_user_by_email(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)

    user = User.objects.get(username = custom_decrypted_username)
    current_site = get_current_site(request)
    mail_subject = "2FA Link via Email - AkirA"
    message = render_to_string('authentication/two_fac_auth_email.html', {
        'user': user,  
        'domain': current_site.domain,  
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    current_user = User.objects.get(username = custom_decrypted_username)
    to_email = current_user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    messages.warning(request, "Please Check Your Email Inbox")
    return redirect('login')

def twofacauth(request, uidb64, token):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    User = get_user_model()
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        get_user_ip_address = UserLoginDetails.objects.filter(user__username=user).order_by('-created_at')[0]
        if str(ip) == str(get_user_ip_address.user_ip_address):
            login(request, user)
            return redirect('login')
        else:
            user.is_active = False
            user.save()
            messages.warning(request, "You don't have access!")
            return redirect('login')
    else:
        return HttpResponse('Link Expired!')

def twofa_verify_user_by_backup_codes(request, username):
    custom_decrypted_username = ""
    for i in range(len(username)):
        custom_decrypted_username += chr(ord(username[i]) - 468)
    try:
        status_2fa = TwoFactorAuth.objects.get(user__username=custom_decrypted_username)
    except TwoFactorAuth.DoesNotExist:
        status_2fa = None
    current_user_2fa_status = 0
    if (status_2fa != None) and (status_2fa.twofa == 0):
        current_user_2fa_status = 0
    elif (status_2fa != None) and (status_2fa.twofa == 1):
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0
    try:
        uvs = UserVerificationStatus.objects.get(user__username=custom_decrypted_username)
    except UserVerificationStatus.DoesNotExist:
        uvs = None
    if uvs != None:
        current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).order_by('-created_at')[0]
    current_userverificationstatus_count = UserVerificationStatus.objects.filter(user__username=custom_decrypted_username).count()
    if (current_user_2fa_status == 0) and ((current_userverificationstatus_count == 0) or (current_userverificationstatus_count > 0 and current_userverificationstatus.status == "Verified")):
        return redirect('login')
    else:
        user = User.objects.get(username = custom_decrypted_username)
        if request.method == 'POST':
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            user_confirm = 0
            backup_code = request.POST.get('backup_code')
            current_user_backup_codes = User_BackUp_Codes.objects.get(user=user)
            backup_codes_with_hash = current_user_backup_codes.backup_codes
            splitup_backup_codes = backup_codes_with_hash.split('#')
            align_backup_code = []
            for i in splitup_backup_codes:
                align_backup_code.append(i)
            if backup_code in align_backup_code:
                user_confirm = 1
                align_backup_code.remove(backup_code)
                join_hash = '#'.join(align_backup_code)
                userbackupcodes = User_BackUp_Codes.objects.get(id=current_user_backup_codes.id)
                userbackupcodes.backup_codes = join_hash
                userbackupcodes.save()
                user = User.objects.get(username = user.username)
                user.is_active = True
                user.save()
                try:
                    user_backup_code_la = User_BackUp_Codes_Login_Attempts.objects.get(user__username=custom_decrypted_username)
                except User_BackUp_Codes_Login_Attempts.DoesNotExist:
                    user_backup_code_la = None
                if user_backup_code_la == None:
                    create_attempt_success = User_BackUp_Codes_Login_Attempts(user = user, attempt = user_confirm, status = "Success")
                    create_attempt_success.save()
                else:
                    get_user_bcla = User_BackUp_Codes_Login_Attempts.objects.get(user__username=custom_decrypted_username)
                    get_user_bcla.attempt = user_confirm
                    get_user_bcla.status = "Success"
                    get_user_bcla.save()
                login(request, user)
                return redirect('login')
            else:
                user_confirm = 2
                update_attempt_failed = User_BackUp_Codes_Login_Attempts(user = user, attempt = user_confirm, status = "Failed")
                update_attempt_failed.save()
                backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(user = user, status = "Failed").count()
                if backup_code_attempt_status_count > 4:
                    block_ip = User_IP_B_List(black_list=ip)
                    block_ip.save()
                else:
                    return redirect('verify_user_by_backup_codes', username=username)
        else:
            return render(request, 'authentication/enter_backup_code.html')

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

# lst = UserVerificationStatus.objects.filter(status="Verified")
# for i in lst:
#     delete_all_records = UserVerificationStatus.objects.get(id=i.id)
#     delete_all_records.delete()

# lst = UserVerificationStatus.objects.filter(status="Have to Verify")
# for i in lst:
#     delete_all_records = UserVerificationStatus.objects.get(id=i.id)
#     delete_all_records.delete()

# user = User.objects.get(username = '4akhi')
# user.is_active = True
# user.save()

# user = User.objects.get(username = 'hari.vege')
# user.is_active = True
# user.save()

# backUpCode = User_BackUp_Codes.objects.all()
# User_BackUp_Codes.objects.all().delete()
# backUpCode = User_BackUp_Codes.objects.all()

# twoauth = TwoFactorAuth.objects.all()
# TwoFactorAuth.objects.all().delete()
# twoauth = TwoFactorAuth.objects.all()

# twoauth = User_BackUp_Codes_Login_Attempts.objects.all()
# User_BackUp_Codes_Login_Attempts.objects.all().delete()
# twoauth = User_BackUp_Codes_Login_Attempts.objects.all()

# import json
# import requests
# ip = '117.207.250.185'
# r = requests.get('https://ipinfo.io/%s/geo' % ip)
# st = (r.content).decode("utf-8")
# res = json.loads(st)
# print(res['city'])
# print(res['region'])
# print(res['country'])

# custom_encrypted_username = ""
# user="4akhi"
# for i in range(len(user)):
#     custom_encrypted_username += chr(ord(user[i]) + 468)
# print(custom_encrypted_username)

# custom_decrypted_username = ""
# username=custom_encrypted_username
# for i in range(len(username)):
#     custom_decrypted_username += chr(ord(username[i]) - 468)
# print(custom_decrypted_username)

# username = 'hari.vege'
# current_userverificationstatus_have_to_verify_count = UserVerificationStatus.objects.filter(user__username=username, status="Have to Verify").count()
# current_userverificationstatus = UserVerificationStatus.objects.filter(user__username=username, status="Have to Verify").order_by('-created_at')
# print(current_userverificationstatus_have_to_verify_count)
# if (current_userverificationstatus_have_to_verify_count == 0) or (current_userverificationstatus[0].status == "Verified"):
#     print("Login")
# else:
#     print("confirm")

# username = 'hari.vege'
# list_codes = secrets.token_urlsafe(45)
# print(list_codes)
# print(len(list_codes))
# split_str = re.findall('.{1,6}', str(list_codes))
# print(split_str)
# join_hash = '#'.join(split_str)
# print(join_hash)
# split_hash = join_hash.split('#')
# print(split_hash)