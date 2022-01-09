from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django import http
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError

import datetime as pydt
import re
import httpagentparser
import json
import requests

from akira_apps.super_admin.decorators import unauthenticated_user
from akira_apps.accounts.models import TwoFactorAuth
from akira_apps.authentication.token import account_activation_token
from . models import (User_BackUp_Codes, User_BackUp_Codes_Login_Attempts, User_IP_S_List, UserLoginDetails, User_IP_B_List, SwitchDevice, UserPageVisits)

from akira_apps.staff.urls import *
from akira_apps.super_admin.urls import *
from akira_apps.academic_registration.urls import *

@unauthenticated_user
def user_login(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    current_time = pydt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        username = request.POST.get('username')
        ep = request.POST.get('password')
        user_ip_address = ip

        try:
            url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
            response = requests.get(url)
            dataUsername = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")
            return redirect('login')

        try:
            url = 'https://akira-rest-api.herokuapp.com/getMetaData/{}/{}/?format=json'.format(username, ep)
            response = requests.get(url)
            data = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")
            return redirect('login')

        try:
            captcha_token=request.POST.get("g-recaptcha-response")
            cap_url="https://www.google.com/recaptcha/api/siteverify"
            cap_secret=settings.GOOGLE_RECAPTCHA_SECRET_KEY
            cap_data={"secret":cap_secret,"response":captcha_token}
            cap_server_response=requests.post(url=cap_url,data=cap_data)
            cap_json=json.loads(cap_server_response.text)
        except Exception:
            messages.info(request, 'Check your internet connection')
            return redirect('login')

        try:
            checkUserExists = User.objects.get(username=username)
        except User.DoesNotExist:
            checkUserExists = None

        user = User.objects.get(username = username)
        
        if cap_json['success'] == True:
            if data['checkKeyEncrypted'] is True:
                if User_IP_S_List.objects.filter(suspicious_list = user_ip_address).exists() is False:
                    if checkUserExists:
                        if user.is_active == True:
                            user = authenticate(request, username=username, password=data['MetaKey'])
                            if user is not None:
                                save_login_details(request, username, user_ip_address, "Not Confirmed Yet!", None)
                                if TwoFactorAuth.objects.filter(user__username = username, twofa = True).exists() is True:
                                    return redirect('twofa_verify_its_you', username=dataUsername['EncryptedUsername'])
                                else:
                                    dataset_UserLoginDetails = UserLoginDetails.objects.filter(user__username=username).count()
                                    if dataset_UserLoginDetails > 2:
                                        current_uld = UserLoginDetails.objects.filter(user__username = username)
                                        old_uld_7 = UserLoginDetails.objects.filter(created_at__lte = pydt.datetime.now() - pydt.timedelta(days=7)).count()
                                        last_current_uld = UserLoginDetails.objects.filter(user__username = username).order_by('-created_at')
                                        current_user = User.objects.get(username=username)
                                        list_current_uld_ipa = []
                                        list_current_uld_osd = []
                                        list_current_uld_bd = []
                                        if len(current_uld) > old_uld_7:
                                            n = len(current_uld) - old_uld_7
                                        else:
                                            n = 0
                                        for i in range(n,len(current_uld)-1):
                                            list_current_uld_ipa.append(current_uld[i].user_ip_address)
                                            list_current_uld_osd.append(current_uld[i].os_details)
                                            list_current_uld_bd.append(current_uld[i].browser_details)

                                        user_ip_address = list(last_current_uld)[0].user_ip_address
                                        os_details = list(last_current_uld)[0].os_details
                                        browser_details = list(last_current_uld)[0].browser_details

                                        count = 0
                                        if user_ip_address in list_current_uld_ipa:
                                            count += 16
                                        if os_details in list_current_uld_osd:
                                            count += 4
                                        if browser_details in list_current_uld_bd:
                                            count += 2
                                        if (count == 22):
                                            login(request, user)
                                            get_attempt_ncy = UserLoginDetails.objects.filter(user__username=user, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                                            update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
                                            update_attempt_ncy.score = count
                                            update_attempt_ncy.attempt = "Success"
                                            update_attempt_ncy.reason = str(count)
                                            update_attempt_ncy.save()
                                            return redirect('login')
                                        elif (count>=4 and count<=20):
                                            get_attempt_ncy = UserLoginDetails.objects.filter(user__username=user, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                                            update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
                                            update_attempt_ncy.score = count
                                            update_attempt_ncy.attempt = "Manual Confirmation Required"
                                            update_attempt_ncy.reason = "Login is unusual"
                                            update_attempt_ncy.user_confirm = "Pending due to unusual login"
                                            update_attempt_ncy.save()
                                            current_site = get_current_site(request)
                                            context = {
                                                "first_name":current_user.first_name,
                                                "email":current_user.email,
                                                "user_ip_address":user_ip_address,
                                                "os_details":os_details,
                                                "browser_details":browser_details,
                                                "current_time":current_time,
                                                "username":dataUsername['EncryptedUsername'],
                                                "domain": current_site.domain,
                                            }
                                            template = render_to_string('authentication/login_alert_email.html', context)
                                            try:
                                                send_mail('Akira Account Login Alert', template, settings.EMAIL_HOST_USER, [current_user.email], html_message=template)
                                                messages.info(request, "Please check your email inbox")
                                            except Exception:
                                                deleteLoginDetails = UserLoginDetails.objects.filter(user__username=user, 
                                                                                                    attempt="Manual Confirmation Required", 
                                                                                                    reason = "Login is unusual",
                                                                                                    user_confirm = "Pending due to unusual login")
                                                deleteLoginDetails.delete()
                                                messages.warning(request, "Check your internet connection")
                                            return redirect('login')
                                        elif count<=2:
                                            user = User.objects.get(username = user.username)
                                            user.is_active = False
                                            user.save()
                                            get_attempt_ncy = UserLoginDetails.objects.filter(user__username=user, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                                            update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
                                            update_attempt_ncy.score = count
                                            update_attempt_ncy.attempt = "Have to Verify"
                                            update_attempt_ncy.reason = str(count)
                                            update_attempt_ncy.save()
                                            return redirect('verify_its_you', username=dataUsername['EncryptedUsername'])
                                    elif dataset_UserLoginDetails < 3:
                                        current_userlogindetailsObject = UserLoginDetails.objects.filter(user__username=username, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                                        get_current_userlogindetailsObject_Id = UserLoginDetails.objects.get(id=current_userlogindetailsObject.id)
                                        get_current_userlogindetailsObject_Id.attempt = "Success"
                                        get_current_userlogindetailsObject_Id.save()
                                        
                                        login(request, user)
                                        group = None
                                        if request.user.groups.exists():
                                            group = request.user.groups.all()[0].name
                                        if group == 'Student':
                                            if (request.GET.get('next')):
                                                return redirect(request.GET.get('next'))
                                            else:
                                                return redirect('student_dashboard')
                                        elif group == 'Assistant Professor':
                                            if (request.GET.get('next')):
                                                return redirect(request.GET.get('next'))
                                            else: 
                                                return redirect('staff_dashboard')
                                        elif group == 'Associate Professor':
                                            if (request.GET.get('next')):
                                                return redirect(request.GET.get('next'))
                                            else: 
                                                return redirect('staff_dashboard')
                                        elif group == 'Professor':
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
                                                return redirect('staff_dashboard')
                                        elif group == 'Administrator':
                                            if (request.GET.get('next')):
                                                return redirect(request.GET.get('next'))
                                            else:
                                                return redirect('super_admin_dashboard')
                            else:
                                messages.warning(request, 'Username or Password is Incorrect!')
                                save_login_details(request, username, user_ip_address, "Failed", "Username or Password is Incorrect!")
                                return redirect('login')
                        else:
                            messages.info(request, 'Your account has been disabled')
                            save_login_details(request, username, user_ip_address, "Need to verify", "User account is disabled")
                            return redirect('verify_its_you', username=dataUsername['EncryptedUsername'])
                    else:
                        messages.warning(request, 'No such account exist!')
                        save_login_details(request, None, user_ip_address, "Failed", "No such account exist!")
                        return redirect('login')
                else:
                    messages.warning(request, 'Login from suspicious IP address')
                    if checkUserExists:
                        save_login_details(request, username, user_ip_address, "Need to verify", "Login attempt from suspicious IP address")
                        return redirect('verify_its_you', username=dataUsername['EncryptedUsername'])
            else:
                messages.warning(request, 'Connection is NOT secured!')
                if checkUserExists:
                    save_login_details(request, username, user_ip_address, "Failed", "Connection is NOT secured")
                    detect_spam_login(request, username, user_ip_address)
                else:
                    save_login_details(request, None, user_ip_address, "Failed", "Connection is NOT secured")
                    detect_spam_login(request, None, user_ip_address)
                return redirect('login')
        else:
            messages.error(request, 'Invalid Captcha try again!')
            if checkUserExists:
                save_login_details(request, username, user_ip_address, "Failed", "Invalid Captcha try again!")
            else:
                save_login_details(request, None, user_ip_address, "Failed", "Invalid Captcha try again!")
            return redirect('login')
    context = {
        "GOOGLE_RECAPTCHA_PUBLIC_KEY":settings.GOOGLE_RECAPTCHA_PUBLIC_KEY,
    }
    return render(request, 'authentication/login.html', context)

def save_login_details(request, user_name, user_ip_address, attempt, reason):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]
    if user_name == None:
        UserLoginDetails.objects.create(user_ip_address=user_ip_address, os_details=OS_Details, browser_details=browser, attempt=attempt, reason=reason)
    else:
        userObj = User.objects.get(username=user_name)
        try:
            UserLoginDetails.objects.create(user_ip_address=user_ip_address, user=userObj, os_details=OS_Details, browser_details=browser, attempt=attempt, reason=reason)
        except Exception as e:
            return e

def verify_its_you(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')
    
    try:
        checkUserBackupCode = User_BackUp_Codes.objects.get(user__username = dataUsername['DecryptedUsername'])
    except User_BackUp_Codes.DoesNotExist:
        checkUserBackupCode = None

    if UserLoginDetails.objects.filter(user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False:
        return redirect('login')
    else:
        context = {
            "username":username,
            "checkUserBackupCode":checkUserBackupCode,
            "custom_decrypted_username":dataUsername['DecryptedUsername'],
        }
        return render(request, 'authentication/verifyItsYou/verify_its_you.html', context)

def verify_user_by_email(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    user = User.objects.get(username=dataUsername['DecryptedUsername'])
    if UserLoginDetails.objects.filter(user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False:
        messages.info(request, "You've been verified, already!")
        return redirect('login')
    else:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        current_site = get_current_site(request)
        mail_subject = "Verify It's You! - AkirA"
        message = render_to_string('authentication/verifyItsYou/user_confirmation_email.html', {
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        current_user = User.objects.get(username = dataUsername['DecryptedUsername'])
        to_email = current_user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        messages.warning(request, "Please Check Your Email Inbox")
        loginAlertContent = {
            "username":username,
        }
        return render(request, 'authentication/loginAlert.html', loginAlertContent)

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
        get_attempt_ncy = UserLoginDetails.objects.filter(user__username=user, attempt="Need to verify").order_by('-created_at')[0]
        update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
        update_attempt_ncy.attempt = "Success"
        update_attempt_ncy.reason = "Verified via Confirm Link via Email"
        update_attempt_ncy.save()
        return HttpResponse("Thank you for confirming your Login")
    else:
        logout(request)
        messages.warning(request, "Link has been expired!")
        return redirect('login')

def confirmEmailStatus(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if UserLoginDetails.objects.filter(user_ip_address = ip, 
                                        user__username = dataUsername['DecryptedUsername'],
                                        attempt="Success", 
                                        reason = "Verified via Confirm Link via Email").exists() is True:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        messages.success(request, "Login Successful")
        login(request, user)
        data = {
            'status': 'success',
        }
    else:
        logout(request)
        data = {
            'status': 'failed',
        }
    response = JsonResponse(data)
    return response

def verify_user_by_backup_codes(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')
    try:
        checkUserBackupCode = User_BackUp_Codes.objects.get(user__username = dataUsername['DecryptedUsername'])
    except User_BackUp_Codes.DoesNotExist:
        checkUserBackupCode = None
    if checkUserBackupCode != None:
        user = User.objects.get(username=dataUsername['DecryptedUsername'])
        if (TwoFactorAuth.objects.filter(user__username = dataUsername['DecryptedUsername'], twofa = True).exists() is True) and (UserLoginDetails.objects.filter(user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False):
            return redirect('login')
        else:
            user = User.objects.get(username = dataUsername['DecryptedUsername'])
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
                    user.is_active = True
                    user.save()
                    get_LoginAttempt = UserLoginDetails.objects.filter(user=user, attempt="Need to verify").order_by('-created_at')[0]
                    update_LoginAttempt = UserLoginDetails.objects.get(id=get_LoginAttempt.id)
                    update_LoginAttempt.attempt = "Success"
                    update_LoginAttempt.reason = "Confirmed User via Backup Codes"
                    update_LoginAttempt.save()
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('login')
                else:
                    user_confirm = 2
                    User_BackUp_Codes_Login_Attempts.objects.create(user = user, attempt = user_confirm, status = "Failed")
                    backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(user = user, status = "Failed").count()
                    if backup_code_attempt_status_count > 4:
                        User_IP_S_List.objects.create(suspicious_list=ip)
                    else:
                        return redirect('verify_user_by_backup_codes', username=username)
            else:
                context = {
                    "custom_decrypted_username":dataUsername['DecryptedUsername'],
                    "en_username":username,
                }
                return render(request, 'authentication/verifyItsYou/enter_backup_code.html', context)
    else:
        messages.info(request, "You don't have backup codes")
        return redirect('verify_its_you', username=username)

def detect_spam_login(request, uid, spam_user_ip_address):
    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
    if uid == None:
        if UserLoginDetails.objects.filter(user_ip_address = spam_user_ip_address, attempt="Failed", reason="Connection is NOT secured", created_at__gte=twenty_four_hrs).exists() is True:
            User_IP_B_List.objects.create(black_list=spam_user_ip_address)
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    else:
        if UserLoginDetails.objects.filter(user__username = uid, user_ip_address = spam_user_ip_address, attempt="Failed", reason="Connection is NOT secured", created_at__gte=twenty_four_hrs).exists() is True:
            user = User.objects.get(username = uid)
            User_IP_B_List.objects.create(black_list=spam_user_ip_address, login_user = user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Re-activate your AkirA account'
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
            messages.warning(request, "Please check your Email inbox")
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
        return HttpResponse('Thank you for Re-activating your account. Now you can login your account.')
    else:  
        return HttpResponse('Activation link is invalid!')

def twofa_verify_its_you(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    try:
        checkUserBackupCode = User_BackUp_Codes.objects.get(user__username = dataUsername['DecryptedUsername'])
    except User_BackUp_Codes.DoesNotExist:
        checkUserBackupCode = None
    
    if TwoFactorAuth.objects.filter(user__username = dataUsername['DecryptedUsername'], twofa = True).exists() is True:
        user = User.objects.get(username=dataUsername['DecryptedUsername'])
        first_name = user.first_name
        context = {
            "username":user,
            "encrypted_username":username,
            "first_name":first_name,
            "checkUserBackupCode":checkUserBackupCode,
        }
        return render(request, 'authentication/twoFactorAuthentication/twofactorauth.html', context)
    else:
        messages.warning(request, "You haven't enabled 2FA!")
        return redirect('login')

# def twofa_verify_user_by_email(request, username):
#     try:
#         url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
#         response = requests.get(url)
#         dataUsername = response.json()
#     except Exception:
#         messages.info(request, "Server under maintenance. Please try again later.")
#         return redirect('login')

#     if TwoFactorAuth.objects.filter(user__username = dataUsername['DecryptedUsername'], twofa = True).exists() is True:
#         user = User.objects.get(username = dataUsername['DecryptedUsername'])
#         current_site = get_current_site(request)
#         mail_subject = "2FA Link via Email - AkirA"
#         message = render_to_string('authentication/twoFactorAuthentication/two_fac_auth_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':account_activation_token.make_token(user),
#         })
#         current_user = User.objects.get(username = dataUsername['DecryptedUsername'])
#         to_email = current_user.email
#         email = EmailMessage(mail_subject, message, to=[to_email])
#         email.send()
#         loginAlert2FAContent = {
#             "username":username,
#         }
#         return render(request, 'authentication/twoFactorAuthentication/loginAlert2FA.html', loginAlert2FAContent)
#     else:
#         messages.warning(request, "You haven't enabled 2FA!")
#         return redirect('login')

# def twofacauth_email(request, uidb64, token):
#     User = get_user_model()
#     try:  
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)  
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         getCurrentLogin = UserLoginDetails.objects.filter(user__username = user, attempt = "Not Confirmed Yet!").order_by('-created_at')[0]
#         UpdateCurrentLoginAttepmt = UserLoginDetails.objects.get(id=getCurrentLogin.id)
#         UpdateCurrentLoginAttepmt.attempt = "Success"
#         UpdateCurrentLoginAttepmt.reason = "Verified via 2FA Email Link"
#         UpdateCurrentLoginAttepmt.save()
#         return HttpResponse("Thank you for confirming your Login")
#     else:
#         logout(request)
#         messages.warning(request, "Link has been expired!")
#         return redirect('login')

# def confirm2FAEmailStatus(request, username):
#     try:
#         url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
#         response = requests.get(url)
#         dataUsername = response.json()
#     except Exception:
#         messages.info(request, "Server under maintenance. Please try again later.")
#         return redirect('login')

#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')

#     if UserLoginDetails.objects.filter(user_ip_address = ip,
#                                         user__username = dataUsername['DecryptedUsername'],
#                                         attempt = "Success",
#                                         reason = "Verified via 2FA Email Link").exists() is True:
#         user = User.objects.get(username = dataUsername['DecryptedUsername'])
#         messages.success(request, "Login Successful")
#         login(request, user)
#         data = {
#             'status': 'success',
#         }
#     else:
#         logout(request)
#         data = {
#             'status': 'failed',
#         }
#     response = JsonResponse(data)
#     return response

def twofa_verify_user_by_backup_codes(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    user = User.objects.get(username=dataUsername['DecryptedUsername'])
    if TwoFactorAuth.objects.filter(user__username = dataUsername['DecryptedUsername'], twofa = False).exists() is True:
        return redirect('login')
    else:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
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
                user.is_active = True
                user.save()
                try:
                    user_backup_code_la = User_BackUp_Codes_Login_Attempts.objects.get(user__username=dataUsername['DecryptedUsername'])
                except User_BackUp_Codes_Login_Attempts.DoesNotExist:
                    user_backup_code_la = None
                if user_backup_code_la == None:
                    User_BackUp_Codes_Login_Attempts.objects.create(user = user, attempt = user_confirm, status = "Success")
                else:
                    get_user_bcla = User_BackUp_Codes_Login_Attempts.objects.get(user__username=dataUsername['DecryptedUsername'])
                    get_user_bcla.attempt = user_confirm
                    get_user_bcla.status = "Success"
                    get_user_bcla.save()
                
                get_LoginAttempt = UserLoginDetails.objects.filter(user=user, attempt="Need to verify").order_by('-created_at')[0]
                update_LoginAttempt = UserLoginDetails.objects.get(id=get_LoginAttempt.id)
                update_LoginAttempt.attempt = "Success"
                update_LoginAttempt.reason = "Confirmed User via 2FA Backup Codes"
                update_LoginAttempt.save()
                login(request, user)
                return redirect('login')
            else:
                user_confirm = 2
                User_BackUp_Codes_Login_Attempts.objects.create(user = user, attempt = user_confirm, status = "Failed")
                backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(user = user, status = "Failed").count()
                if backup_code_attempt_status_count > 4:
                    User_IP_S_List.objects.create(suspicious_list=ip)
                else:
                    return redirect('twofa_verify_user_by_backup_codes', username=username)
        context = {
            "custom_decrypted_username":dataUsername['DecryptedUsername'],
            "encrypted_username":username,
        }
        return render(request, 'authentication/twoFactorAuthentication/two_fac_enter_backup_code.html', context)

def confirmUserLogin(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')
    try:
        get_attempt_ARU = UserLoginDetails.objects.get(
                        user__username=username, 
                        attempt="Manual Confirmation Required",
                        reason = "Login is unusual",
                        user_confirm = "Pending due to unusual login")
    except UserLoginDetails.DoesNotExist:
        get_attempt_ARU = None
    if get_attempt_ARU:
        context = {
            "username":dataUsername['EncryptedUsername'],
        }
        return render(request, 'authentication/confirmUserLogin.html', context)
    else:
        messages.info(request, "User is already confirmed!")
        return redirect('login')

def secure_account(request, username, user_response):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    try:
        get_attempt_ARU = UserLoginDetails.objects.get(
                        user__username=dataUsername['DecryptedUsername'], 
                        attempt="Manual Confirmation Required",
                        reason = "Login is unusual",
                        user_confirm = "Pending due to unusual login")
    except UserLoginDetails.DoesNotExist:
        get_attempt_ARU = None
    if get_attempt_ARU != None:
        get_attempt_ARU = UserLoginDetails.objects.get(
                        user__username=dataUsername['DecryptedUsername'], 
                        attempt="Manual Confirmation Required",
                        reason = "Login is unusual",
                        user_confirm = "Pending due to unusual login")
        if get_attempt_ARU.user.username == dataUsername['DecryptedUsername']:
            if user_response == "yes":
                get_attempt_ARU = UserLoginDetails.objects.filter(user__username=dataUsername['DecryptedUsername'], attempt="Manual Confirmation Required").order_by('-created_at')[0]
                get_attempt_ARU.attempt = "Success"
                get_attempt_ARU.user_confirm = "Login Confirmed"
                get_attempt_ARU.reason = "Login Confirmed via Email Manually"
                get_attempt_ARU.save()
                user = User.objects.get(username = dataUsername['DecryptedUsername'])
                user.is_active = True
                user.save()
                return redirect('login')
            else:
                logout(request)
                return redirect('login')
        else:
            logout(request)
            return redirect('login')
    else:
        logout(request)
        return redirect('login')

def checkUserResponse(request, username):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        userLoginDetails = UserLoginDetails.objects.get(
                        user__username = dataUsername['DecryptedUsername'], 
                        attempt="Success",
                        user_confirm = "Login Confirmed",
                        reason = "Login Confirmed via Email Manually")
    except UserLoginDetails.DoesNotExist:
        userLoginDetails = None
    if (userLoginDetails != None) and (userLoginDetails.user_ip_address == ip):
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        login(request, user)
        data = {
            'status': 'success',
        }
    else:
        logout(request)
        data = {
            'status': 'failed',
        }
    response = JsonResponse(data)
    return response

def requestSwitchDevice(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]

    if request.method == 'POST':
        currentUserIPAddr = request.POST.get('user_ip_address')
        currentUserBrowser = request.POST.get('user_browser')
        currentUserOS = request.POST.get('user_os')
        currentUsername = request.POST.get('username')
        getUserObject = User.objects.get(username = currentUsername)
        try:
            SwitchDevice.objects.create(
                    userIPAddr = currentUserIPAddr,
                    userBrowser = currentUserBrowser,
                    userOS = currentUserOS,
                    reason = "Not Approved Yet",
                    user = getUserObject)
        except IntegrityError:
            messages.info(request, "You have already requested to switch device!")
            print("You have already requested to switch device!")

        PostContext = {
            "currentUsername":currentUsername,
        }
        return render(request, 'authentication/SwitchDevice/waitingSwitchDeviceResponse.html', PostContext)
    context = {
        "CurrentUserIPAddr":ip,
        "CurrentBrowser":browser,
        "CurrentOS":OS_Details,
    }
    return render(request, 'authentication/SwitchDevice/requestSwitchDevice.html', context)

def validateSwitchDevice(request):
    try:
        get_SwitchDeviceRequest = SwitchDevice.objects.get(
                                            user__username=request.user.username,
                                            reason = "Not Approved Yet",
                                            userConfirm = "Pending")
    except SwitchDevice.DoesNotExist:
        get_SwitchDeviceRequest = None
    if request.method == "POST":
        if get_SwitchDeviceRequest != None:
            get_SwitchDeviceRequest = SwitchDevice.objects.get(
                            user__username=request.user.username,
                            reason = "Not Approved Yet",
                            userConfirm = "Pending")
            if get_SwitchDeviceRequest.user.username == request.user.username:
                getLastPage = UserPageVisits.objects.filter(user__username=request.user.username).order_by('-created_at')[0]
                update_SwitchDeviceRequest = SwitchDevice.objects.filter(user__username=request.user.username, 
                                                            reason = "Not Approved Yet",
                                                            userConfirm = "Pending",
                                                            status="Switch Device Pending").order_by('-created_at')[0]
                update_SwitchDeviceRequest.userConfirm = "User Approved"
                update_SwitchDeviceRequest.reason = "User Confirmed the Switch Device"
                update_SwitchDeviceRequest.currentPage = getLastPage.currentPage
                update_SwitchDeviceRequest.save()
                user = User.objects.get(username = request.user.username)
                user.is_active = True
                user.save()
                # return HttpResponse("Your Approval Request is been taken successfully")
                postContext = {
                    "get_SwitchDeviceRequest":get_SwitchDeviceRequest,
                    "SwitchDeviceStatus":True,
                }
                return render(request, 'authentication/SwitchDevice/acceptSwitchDevice.html', postContext)
        else:
            logout(request)
            return HttpResponse("No Switch Device Request Found!")
    Context = {
        "get_SwitchDeviceRequest":get_SwitchDeviceRequest,
        "SwitchDeviceStatus":False,
    }
    return render(request, 'authentication/SwitchDevice/acceptSwitchDevice.html', Context)

def checkValidatedSwitchDeviceRequest(request, username):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        GetSwitchDeviceRequestObject = SwitchDevice.objects.get(
                        user__username=username, 
                        userConfirm = "User Approved",
                        reason = "User Confirmed the Switch Device",
                        status="Switch Device Pending")
    except SwitchDevice.DoesNotExist:
        GetSwitchDeviceRequestObject = None
    if (GetSwitchDeviceRequestObject != None) and (GetSwitchDeviceRequestObject.userIPAddr == ip):
        user = User.objects.get(username = username)
        currentUrl = GetSwitchDeviceRequestObject.currentPage
        login(request, user)
        data = {
            'status': 'success',
            'redirect_url':currentUrl,
        }
    else:
        logout(request)
        data = {
            'status': 'failed',
        }
    response = JsonResponse(data)
    return response

def SwitchDeviceStatus(request, username):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        GetSwitchDeviceRequestObject = SwitchDevice.objects.get(
                        user__username=username, 
                        userConfirm = "User Approved",
                        reason = "User Confirmed the Switch Device",
                        status="Switch Device Pending")
    except SwitchDevice.DoesNotExist:
        GetSwitchDeviceRequestObject = None
    if (GetSwitchDeviceRequestObject != None) and (GetSwitchDeviceRequestObject.userIPAddr == ip):
        update_SwitchDeviceStatus = SwitchDevice.objects.filter(user__username=request.user.username, 
                                                    reason = "User Confirmed the Switch Device",
                                                    userConfirm = "User Approved",
                                                    status="Switch Device Pending").order_by('-created_at')[0]
        update_SwitchDeviceStatus.userIPAddr = ip
        update_SwitchDeviceStatus.status = "Switch Device Successful"
        update_SwitchDeviceStatus.save()
        return "Switch Device Successful"
    else:
        return HttpResponse("No Switch Device Request Found!")

def SyncDevice(request):
    getSecondDevice = SwitchDevice.objects.filter(
                            user__username = request.user.username,
                            status = "Switch Device Successful",
                            userConfirm = "User Approved").order_by('-created_at')[0]
    getSecondDeviceCurrentPage = UserPageVisits.objects.filter(
                                user__username = request.user.username,
                                userIPAddr = getSecondDevice.userIPAddr).order_by('-created_at')[0]
    return redirect(getSecondDeviceCurrentPage.currentPage)


# SwitchDevice.objects.all().delete()
# UserPageVisits.objects.all().delete()

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')