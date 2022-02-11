from django import http
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

import datetime as pydt
import re
import httpagentparser
import json
import requests
import string
import random
import math

from akira_apps.super_admin.decorators import unauthenticated_user
from akira_apps.accounts.models import TwoFactorAuth
from akira_apps.authentication.token import account_activation_token
from . models import (User_BackUp_Codes, User_BackUp_Codes_Login_Attempts, 
                        User_IP_S_List, UserLoginDetails, User_IP_B_List, 
                        SwitchDevice, UserPageVisits)

from akira_apps.staff.urls import *
from akira_apps.super_admin.urls import *
from akira_apps.academic_registration.urls import *

def TestingArea(request):
    decipherText = ''
    plainPassword = ''
    username = ''
    if request.method == "POST":
        username = request.POST.get('username')
        encryptedText = request.POST.get('deciphertext')
        plainPassword = request.POST.get('password')
        
        encryptedTextLength = len(encryptedText)
        print(encryptedTextLength)

        ASCII_Username = []
        for i in username:
            ASCII_Username.append(ord(i))

        ASCII_Username_Sum = list(map(int, str(sum(ASCII_Username))))
        print(ASCII_Username_Sum)

        # If ASCII_Username_Sum contains any element zero, then replace those zero with 1
        for i in range(len(ASCII_Username_Sum)):
            if ASCII_Username_Sum[i] == 0:
                ASCII_Username_Sum[i] = 1
        print(ASCII_Username_Sum)

        # First Largest Number in ASCII_Username_Sum
        max_ASCII_Username_Sum = max(ASCII_Username_Sum)
        print("max_ASCII_Username_Sum: ", max_ASCII_Username_Sum)

        # Second Largest Number in ASCII_Username_Sum
        def findLargest(arr):
            a=arr
            a=list(set(a))
            a.sort()
            if(len(a)==1 ):
                return (a[0]+1)
            else:
                return (a[-2])

        second_largest = findLargest(ASCII_Username_Sum)
        print("Second Largest", second_largest)

        # if second_largest is zero or not finite then replace it with max(ASCII_Username_Sum) + 1
        if second_largest == 0 or math.isinf(second_largest) or second_largest == -math.inf or second_largest == max_ASCII_Username_Sum:
            second_largest = max_ASCII_Username_Sum + 1
        print("Second Largest",second_largest)

        # Finding the Password length
        lengthUsername10 = len(username) * 10
        password_length = encryptedTextLength / lengthUsername10
        print("Password Length",password_length)

        passwordLength10 = password_length * 10
        print("Password Length 10 Times",passwordLength10)

        # Divide the encrypted text into password_length value parts and store it in a list
        encryptedText_list = []
        for i in range(int(password_length)):
            encryptedText_list.append(encryptedText[i*int(lengthUsername10):(i+1)*int(lengthUsername10)])
        print("Encrypted Text Break Down",encryptedText_list)

        # Find the random digits in the encryptedText_list
        randomDigits = []
        # Store the last nth character of each element in the encryptedText_list in randomDigits list
        for i in range(len(encryptedText_list)):
            randomDigits.append(encryptedText_list[i][-second_largest])
        print("Random Digits",randomDigits)

        # get the elements of the encryptedText_list at specific index using randomDigits elements as index values and store it in a list name final_list
        HexList = []
        for i in range(len(encryptedText_list)):
            HexList.append(encryptedText_list[i][int(randomDigits[i])]+encryptedText_list[i][int(randomDigits[i])+1])
        print(HexList)

        # Convert the HexList elements to ASCII and store it in a final_list
        final_list = []
        for i in range(len(HexList)):
            final_list.append(chr(int(HexList[i], 16)))
        print(final_list)

        Plain_password = []
        for i in final_list:
            value = max_ASCII_Username_Sum + int(max(randomDigits))
            Plain_password.append(chr(ord(i) - value))
        print(Plain_password)
        decipherText = "".join(Plain_password)
    context = {
        'decipherText': decipherText,
        'plainPassword':plainPassword,
        'username':username,
    }
    return render(request, 'TestingArea.html', context)

def DecryptEncryptedCookie(request, username, EncryptedCookie):
    isEncryptedCookie = "Invalid Cookie"
    try:
        EncryptedCookieList = []
        for i in range(0,len(username)):
            EncryptedCookieList.append(EncryptedCookie[i*10:(i+1)*10])

        randomDigits = []
        for i in range(len(EncryptedCookieList)):
            randomDigits.append(EncryptedCookieList[i][-2])

        HexList = []
        for i in range(len(EncryptedCookieList)):
            HexList.append(EncryptedCookieList[i][int(randomDigits[i])]+EncryptedCookieList[i][int(randomDigits[i])+1])

        final_list = []
        for i in range(len(HexList)):
            final_list.append(chr(int(HexList[i], 16)))

        final_list_hex_str = "".join(final_list)
        if username == final_list_hex_str:
            isEncryptedCookie = True
        else:
            isEncryptedCookie = "Invalid Cookie"
        return isEncryptedCookie
    except Exception:
        return isEncryptedCookie

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
        fingerprintID = request.POST.get('fingerprint')
        user_ip_address = ip

        if not re.match(r'[a-zA-Z0-9]{8,}$', username) and re.match(r'[a-zA-Z0-9]{8,}$', ep):
            messages.info(request, 'Please enter a valid credentials.')
            return redirect('login')

        try:
            captcha_token = request.POST.get("g-recaptcha-response")
            cap_url = "https://www.google.com/recaptcha/api/siteverify"
            cap_secret = settings.GOOGLE_RECAPTCHA_SECRET_KEY
            cap_data = {"secret": cap_secret, "response": captcha_token}
            cap_server_response = requests.post(url = cap_url, data = cap_data)
            cap_json = json.loads(cap_server_response.text)
        except Exception:
            messages.info(request, 'Check your internet connection')
            return redirect('login')

        try:
            url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(username)
            response = requests.get(url)
            dataUsername = response.json()
        except Exception:
            messages.info(request, "Server under maintenance. Please try again later.")
            return redirect('login')

        try:
            checkUserExists = User.objects.get(username = username)
        except User.DoesNotExist:
            checkUserExists = None

        try:
            getEncryptedCookie = request.COOKIES['access_token']
        except Exception:
            getEncryptedCookie = "Doesn't Exist"

        if getEncryptedCookie:
            DECookie = DecryptEncryptedCookie(request, username, getEncryptedCookie)

        if cap_json['success'] == True:
            try:
                getMetaDataUrl = 'https://akira-rest-api.herokuapp.com/getMetaData/{}/{}/?format=json'.format(username, ep)
                getMetaDataUrlResponse = requests.get(getMetaDataUrl)
                getMetaDataUrlResponsedata = getMetaDataUrlResponse.json()
            except Exception:
                messages.info(request, "Server under maintenance. Please try again later.")
                return redirect('login')
            if User_IP_S_List.objects.filter(suspicious_list = user_ip_address).exists() is False or DECookie is True:
                if checkUserExists:
                    user = User.objects.get(username = username)
                    try:
                        checkSD = SwitchDevice.objects.get(user = user, status = "Switch Device Successful")
                    except SwitchDevice.DoesNotExist:
                        checkSD = None
                    if checkSD:
                        updatecheckSD = SwitchDevice.objects.filter(user = user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Successful")[0]
                        updatecheckSD.reason = "User Logged In"
                        updatecheckSD.status = "Terminated"
                        updatecheckSD.save()
                    try:
                        checkSDPNA = SwitchDevice.objects.get(user = user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending")
                    except SwitchDevice.DoesNotExist:
                        checkSDPNA = None
                    if checkSDPNA:
                        updatecheckSDPNA = SwitchDevice.objects.get(user = user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending")
                        updatecheckSDPNA.userConfirm = "User Denied"
                        updatecheckSDPNA.reason = "User Logged In"
                        updatecheckSDPNA.status = "Terminated"
                        updatecheckSDPNA.save()
                    if user.is_active == True:
                        user = authenticate(request, username = username, password = getMetaDataUrlResponsedata['MetaKey'])
                        if user is not None:
                            getuserLoginObj = save_login_details(request, username, user_ip_address, fingerprintID, "Not Confirmed Yet!", None)
                            if TwoFactorAuth.objects.filter(user__username = username, twofa = True).exists() is True:
                                return redirect('twofa_verify_its_you', username = dataUsername['EncryptedUsername'], userLoginObj = getuserLoginObj.id)
                            else:
                                dataset_UserLoginDetails = UserLoginDetails.objects.filter(user__username = username)
                                if dataset_UserLoginDetails.count() > 1:
                                    current_user = User.objects.get(username = username)
                                    currentULLCookieObj = UserLoginDetails.objects.filter(user__username = username).last()
                                    if currentULLCookieObj.Logoutcookie == getEncryptedCookie:
                                        LogoutCookie = True
                                    else:
                                        LogoutCookie = False
                                    if UserLoginDetails.objects.filter(user__username = username, bfp = fingerprintID, attempt = "Success").exists() is True or LogoutCookie is True:
                                        login(request, user)
                                        get_attempt_ncy = UserLoginDetails.objects.filter(id = getuserLoginObj.id, user__username = username, attempt = "Not Confirmed Yet!").order_by('-created_at')[0]
                                        update_attempt_ncy = UserLoginDetails.objects.get(id = get_attempt_ncy.id)
                                        update_attempt_ncy.attempt = "Success"
                                        update_attempt_ncy.reason = "BFP ID Matched"
                                        update_attempt_ncy.sessionKey = request.session.session_key
                                        update_attempt_ncy.save()
                                        return redirect('login')
                                    else:
                                        return redirect('verify_its_you', username = dataUsername['EncryptedUsername'], userLoginObj = getuserLoginObj.id)
                                        # get_attempt_ncy = UserLoginDetails.objects.filter(id = getuserLoginObj.id, user__username = username, attempt = "Not Confirmed Yet!").order_by('-created_at')[0]
                                        # update_attempt_ncy = UserLoginDetails.objects.get(id = get_attempt_ncy.id)
                                        # update_attempt_ncy.attempt = "Manual Confirmation Required"
                                        # update_attempt_ncy.reason = "Login is unusual"
                                        # update_attempt_ncy.user_confirm = "Pending due to unusual login"
                                        # update_attempt_ncy.save()
                                        # current_site = get_current_site(request)
                                        # template = render_to_string('authentication/login_alert_email.html', context)
                                        # try:
                                        #     send_mail('Akira Account Login Alert', template, settings.EMAIL_HOST_USER, [current_user.email], html_message=template)
                                        #     messages.info(request, "Please check your email inbox")
                                        #     return redirect('confirmUserLogin', username = dataUsername['EncryptedUsername'], userLoginObj = getuserLoginObj.id)
                                        # except Exception:
                                        #     deleteLoginDetails = UserLoginDetails.objects.filter(id = getuserLoginObj.id, user__username = username, 
                                        #                                                         attempt = "Manual Confirmation Required", 
                                        #                                                         reason = "Login is unusual",
                                        #                                                         user_confirm = "Pending due to unusual login")
                                        #     deleteLoginDetails.delete()
                                        #     messages.warning(request, "Check your internet connection")
                                        #     return redirect('login')
                                else:
                                    login(request, user)
                                    current_userlogindetailsObject = UserLoginDetails.objects.filter(id = getuserLoginObj.id, user__username = username, attempt = "Not Confirmed Yet!").order_by('-created_at')[0]
                                    get_current_userlogindetailsObject_Id = UserLoginDetails.objects.get(id = current_userlogindetailsObject.id)
                                    get_current_userlogindetailsObject_Id.attempt = "Success"
                                    get_current_userlogindetailsObject_Id.sessionKey = request.session.session_key
                                    get_current_userlogindetailsObject_Id.save()
                                    
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
                                        return HttpResponse("Contact Administrator")
                        else:
                            messages.warning(request, 'Username or Password is Incorrect!')
                            save_login_details(request, username, user_ip_address, fingerprintID, "Failed", "Username or Password is Incorrect!")
                            return redirect('login')
                    else:
                        messages.info(request, 'Your account has been disabled')
                        getuserLoginObj = save_login_details(request, username, user_ip_address, fingerprintID, "Need to verify", "User account is disabled")
                        return redirect('verify_its_you', username = dataUsername['EncryptedUsername'], userLoginObj = getuserLoginObj.id)
                else:
                    messages.warning(request, 'No such account exist!')
                    save_login_details(request, None, user_ip_address, fingerprintID, "Failed", "No such account exist!")
                    return redirect('login')
            elif  User_IP_S_List.objects.filter(suspicious_list = user_ip_address).exists() is True or DECookie is False:
                messages.warning(request, 'Suspicious Activity Found!')
                if checkUserExists:
                    getuserLoginObj = save_login_details(request, username, user_ip_address, fingerprintID, "Need to verify", "Suspicious Activity")
                    return redirect('verify_its_you', username = dataUsername['EncryptedUsername'], userLoginObj = getuserLoginObj.id)
        else:
            messages.error(request, 'Invalid Captcha try again!')
            if checkUserExists:
                save_login_details(request, username, user_ip_address, fingerprintID, "Failed", "Invalid Captcha try again!")
            else:
                save_login_details(request, None, user_ip_address, fingerprintID, "Failed", "Invalid Captcha try again!")
            return redirect('login')
    context = {
        "GOOGLE_RECAPTCHA_PUBLIC_KEY": settings.GOOGLE_RECAPTCHA_PUBLIC_KEY,
    }
    loginResponse = render(request, 'authentication/login.html', context)
    random_number = random.randint(48, 68)
    ranKey = ''.join(random.choices(string.ascii_letters + string.digits, k=random_number))
    ranNumberLength = math.ceil((0.18) * len(ranKey))
    ranNumbers = set(random.choices(string.digits, k=ranNumberLength))    
    cookie_max_age = 300
    expire_time = pydt.datetime.strftime(pydt.datetime.utcnow() + pydt.timedelta(seconds=cookie_max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    loginResponse.set_cookie(key='request_token', value=str(ranKey), max_age=cookie_max_age, expires=expire_time)
    return loginResponse

def save_login_details(request, user_name, user_ip_address, fingerprintID, attempt, reason):
    user_agent = request.META['HTTP_USER_AGENT']
    browser = httpagentparser.detect(user_agent)
    if not browser:
        browser = user_agent.split('/')[0]
    else:
        browser = browser['browser']['name']

    res = re.findall(r'\(.*?\)', user_agent)
    OS_Details = res[0][1:-1]
    if user_name == None:
        userLoginObj = UserLoginDetails.objects.create(
                                    user_ip_address = user_ip_address,
                                    bfp = fingerprintID,
                                    os_details = OS_Details,
                                    browser_details = browser,
                                    attempt = attempt, reason = reason)
    else:
        userObj = User.objects.get(username=user_name)
        userLoginObj = UserLoginDetails.objects.create(
                                    user = userObj,
                                    user_ip_address = user_ip_address,
                                    bfp = fingerprintID,
                                    os_details = OS_Details,
                                    browser_details = browser,
                                    attempt = attempt, reason = reason)
    return userLoginObj

def getLoginScore(LoginObjectID, username):
    current_uld = UserLoginDetails.objects.filter(user__username = username, attempt = "Success")
    last_current_uld = UserLoginDetails.objects.get(id = LoginObjectID)
    list_current_uld_ipa = []
    list_current_uld_osd = []
    list_current_uld_bd = []
    for i in range(len(current_uld)-1):
        list_current_uld_ipa.append(current_uld[i].user_ip_address)
        list_current_uld_osd.append(current_uld[i].os_details)
        list_current_uld_bd.append(current_uld[i].browser_details)

    user_ip_address = str(last_current_uld.user_ip_address)
    os_details = str(last_current_uld.os_details)
    browser_details = str(last_current_uld.browser_details)

    count = 0
    if user_ip_address in list_current_uld_ipa:
        count += 16
    if os_details in list_current_uld_osd:
        count += 4
    if browser_details in list_current_uld_bd:
        count += 2
    return count

def verify_its_you(request, username, userLoginObj):
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

    if UserLoginDetails.objects.filter(id = userLoginObj, user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False:
        return redirect('login')
    else:
        context = {
            "username": username,
            "checkUserBackupCode": checkUserBackupCode,
            "custom_decrypted_username": dataUsername['DecryptedUsername'],
            "userLoginObj":userLoginObj,
        }
        return render(request, 'authentication/verifyItsYou/verify_its_you.html', context)

def verify_user_by_email(request, username, userLoginObj):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    user = User.objects.get(username = dataUsername['DecryptedUsername'])
    if UserLoginDetails.objects.filter(id = userLoginObj, user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False:
        messages.info(request, "You've been verified, already!")
        return redirect('login')
    else:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        current_site = get_current_site(request)
        mail_subject = "Verify It's You! - AkirA"
        message = render_to_string('authentication/verifyItsYou/user_confirmation_email.html', {
            'user': user,  
            'domain': current_site.domain,  
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'userLoginObj':userLoginObj,
        })
        current_user = User.objects.get(username = dataUsername['DecryptedUsername'])
        to_email = current_user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        messages.warning(request, "Please Check Your Email Inbox")
        loginAlertContent = {
            "username": username,
            "userLoginObj":userLoginObj,
        }
        return render(request, 'authentication/loginAlert.html', loginAlertContent)

def confirm(request, uidb64, token, userLoginObj):
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
            get_attempt_ncy = UserLoginDetails.objects.filter(id = userLoginObj, user__username = user, attempt = "Need to verify").order_by('-created_at')[0]
        except Exception:
            return HttpResponse(status = 410)
        update_attempt_ncy = UserLoginDetails.objects.get(id=get_attempt_ncy.id)
        update_attempt_ncy.attempt = "Success"
        update_attempt_ncy.reason = "Verified via Confirm Link via Email"
        update_attempt_ncy.save()
        return HttpResponse("Thank you for confirming your Login")
    else:
        logout(request)
        messages.warning(request, "Link has been expired!")
        return redirect('login')

def confirmEmailStatus(request, username, userLoginObj):
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

    if UserLoginDetails.objects.filter(id = userLoginObj, user_ip_address = ip, 
                                        user__username = dataUsername['DecryptedUsername'],
                                        attempt = "Success", 
                                        reason = "Verified via Confirm Link via Email").exists() is True:
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        messages.success(request, "Login Successful")
        login(request, user)
        getUserLoginDetailsObj = UserLoginDetails.objects.get(id = userLoginObj, user_ip_address = ip, 
                                        user__username = dataUsername['DecryptedUsername'],
                                        attempt = "Success", 
                                        reason = "Verified via Confirm Link via Email")
        getUserLoginDetailsObj.sessionKey = request.session.session_key
        getUserLoginDetailsObj.score = getLoginScore(userLoginObj, dataUsername['DecryptedUsername'])
        getUserLoginDetailsObj.save()
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

def verify_user_by_backup_codes(request, username, userLoginObj):
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
        if (UserLoginDetails.objects.filter(id = userLoginObj, user__username = dataUsername['DecryptedUsername'], attempt = "Need to verify").exists() is False):
            return redirect('login')
        else:
            user = User.objects.get(username = dataUsername['DecryptedUsername'])
            if request.method == 'POST':
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                backup_code = request.POST.get('backup_code')
                current_user_backup_codes = User_BackUp_Codes.objects.get(user=user)
                backup_codes_with_hash = current_user_backup_codes.backup_codes
                splitup_backup_codes = backup_codes_with_hash.split('#')
                align_backup_code = []
                for i in splitup_backup_codes:
                    align_backup_code.append(i)
                if backup_code in align_backup_code:
                    align_backup_code.remove(backup_code)
                    join_hash = '#'.join(align_backup_code)
                    userbackupcodes = User_BackUp_Codes.objects.get(id = current_user_backup_codes.id)
                    userbackupcodes.backup_codes = join_hash
                    userbackupcodes.save()
                    user.is_active = True
                    user.save()
                    login(request, user)
                    get_LoginAttempt = UserLoginDetails.objects.filter(id = userLoginObj, user=user, attempt="Need to verify").order_by('-created_at')[0]
                    update_LoginAttempt = UserLoginDetails.objects.get(id=get_LoginAttempt.id)
                    update_LoginAttempt.score = getLoginScore(update_LoginAttempt.id, dataUsername['DecryptedUsername'])
                    update_LoginAttempt.attempt = "Success"
                    update_LoginAttempt.user_confirm = "User used 2FA Backup Codes"
                    update_LoginAttempt.reason = "Confirmed User via Backup Codes"
                    update_LoginAttempt.sessionKey = request.session.session_key
                    update_LoginAttempt.save()
                    checkBackupCodesLength = len(userbackupcodes.backup_codes)
                    if checkBackupCodesLength == 0:
                        return redirect('delete_existing_backup_codes')
                    messages.success(request, "Login Successful")
                    return redirect('login')
                else:
                    messages.info(request, "Invalid Backup Code")
                    User_BackUp_Codes_Login_Attempts.objects.create(user = user, userIPAddr = ip, status = "Failed")
                    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
                    backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(
                                                            user = user, userIPAddr = ip, 
                                                            status = "Failed", 
                                                            created_at__gte=twenty_four_hrs).count()
                    if backup_code_attempt_status_count > 4:
                        User_IP_S_List.objects.create(suspicious_list = ip)
                        messages.info("Please confirm it's you to login")
                        return redirect('login')
                    else:
                        return redirect('verify_user_by_backup_codes', username = username)
            else:
                context = {
                    "custom_decrypted_username": dataUsername['DecryptedUsername'],
                    "en_username": username,
                    "userLoginObj": userLoginObj,
                }
                return render(request, 'authentication/verifyItsYou/enter_backup_code.html', context)
    else:
        messages.info(request, "You don't have backup codes")
        return redirect('verify_its_you', username=username)

def detect_spam_login(request, uid, spam_user_ip_address):
    twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
    if uid == None:
        if UserLoginDetails.objects.filter(user_ip_address = spam_user_ip_address, attempt = "Failed", reason = "Connection is NOT secured", created_at__gte=twenty_four_hrs).exists() is True:
            User_IP_B_List.objects.create(black_list = spam_user_ip_address)
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')
    else:
        if UserLoginDetails.objects.filter(user__username = uid, user_ip_address = spam_user_ip_address, attempt = "Failed", reason = "Connection is NOT secured", created_at__gte = twenty_four_hrs).exists() is True:
            user = User.objects.get(username = uid)
            User_IP_B_List.objects.create(black_list=spam_user_ip_address, login_user = user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Re-activate your AkirA account'
            message = render_to_string('authentication/acc_active_email.html', {
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
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
        user = User.objects.get(pk = uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for Re-activating your account. Now you can login your account.')
    else:  
        return HttpResponse('Link has been expired!')

def twofa_verify_its_you(request, username, userLoginObj):
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
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        first_name = user.first_name
        context = {
            "encrypted_username": username,
            "username": dataUsername['DecryptedUsername'],
            "first_name": first_name,
            "checkUserBackupCode": checkUserBackupCode,
            "userLoginObj":userLoginObj,
        }
        return render(request, 'authentication/twoFactorAuthentication/twofactorauth.html', context)
    else:
        messages.warning(request, "You haven't enabled 2FA!")
        return redirect('login')

def twofa_verify_user_by_backup_codes(request, username, userLoginObj):
    try:
        url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
        response = requests.get(url)
        dataUsername = response.json()
    except Exception:
        messages.info(request, "Server under maintenance. Please try again later.")
        return redirect('login')

    user = User.objects.get(username = dataUsername['DecryptedUsername'])
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
            backup_code = request.POST.get('backup_code')
            current_user_backup_codes = User_BackUp_Codes.objects.get(user=user)
            backup_codes_with_hash = current_user_backup_codes.backup_codes
            splitup_backup_codes = backup_codes_with_hash.split('#')
            align_backup_code = []
            for i in splitup_backup_codes:
                align_backup_code.append(i)
            if backup_code in align_backup_code:
                align_backup_code.remove(backup_code)
                join_hash = '#'.join(align_backup_code)
                userbackupcodes = User_BackUp_Codes.objects.get(id = current_user_backup_codes.id)
                userbackupcodes.backup_codes = join_hash
                userbackupcodes.save()
                user.is_active = True
                user.save()
                login(request, user)
                get_LoginAttempt = UserLoginDetails.objects.filter(id =userLoginObj, user=user, attempt="Not Confirmed Yet!").order_by('-created_at')[0]
                update_LoginAttempt = UserLoginDetails.objects.get(id=get_LoginAttempt.id)
                update_LoginAttempt.score = getLoginScore(update_LoginAttempt.id, dataUsername['DecryptedUsername'])
                update_LoginAttempt.attempt = "Success"
                update_LoginAttempt.user_confirm = "User used 2FA Backup Codes"
                update_LoginAttempt.reason = "Confirmed User via 2FA Backup Codes"
                update_LoginAttempt.sessionKey = request.session.session_key
                update_LoginAttempt.save()
                checkBackupCodesLength = len(userbackupcodes.backup_codes)
                if checkBackupCodesLength == 0:
                    return redirect('delete_existing_backup_codes')
                messages.success(request, "Login Successful")
                return redirect('login')
            else:
                messages.info(request, "Invalid Backup Code")
                User_BackUp_Codes_Login_Attempts.objects.create(user = user, userIPAddr = ip, status = "Failed")
                twenty_four_hrs = pydt.datetime.now() - pydt.timedelta(days=1)
                backup_code_attempt_status_count = User_BackUp_Codes_Login_Attempts.objects.filter(
                                                        user = user, userIPAddr = ip, 
                                                        status = "Failed", 
                                                        created_at__gte=twenty_four_hrs).count()
                if backup_code_attempt_status_count > 4:
                    User_IP_S_List.objects.create(suspicious_list = ip)
                    messages.info("Please confirm it's you to login")
                    return redirect('login')
                else:
                    return redirect('twofa_verify_user_by_backup_codes', username = username)
        context = {
            "custom_decrypted_username": dataUsername['DecryptedUsername'],
            "encrypted_username": username,
            "userLoginObj":userLoginObj,
        }
        return render(request, 'authentication/twoFactorAuthentication/two_fac_enter_backup_code.html', context)

# def confirmUserLogin(request, username, userLoginObj):
#     try:
#         url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
#         response = requests.get(url)
#         dataUsername = response.json()
#     except Exception:
#         messages.info(request, "Server under maintenance. Please try again later.")
#         return redirect('login')
#     try:
#         get_attempt_ARU = UserLoginDetails.objects.get(
#                         id = userLoginObj,
#                         user__username = dataUsername['DecryptedUsername'],
#                         attempt = "Manual Confirmation Required",
#                         reason = "Login is unusual",
#                         user_confirm = "Pending due to unusual login")
#     except UserLoginDetails.DoesNotExist:
#         get_attempt_ARU = None
#     if get_attempt_ARU:
#         context = {
#             "username": username,
#             "userLoginObj":userLoginObj,
#         }
#         return render(request, 'authentication/confirmUserLogin.html', context)
#     else:
#         messages.info(request, "User is already confirmed!")
#         return redirect('login')

# def secure_account(request, username, user_response, userLoginObj):
#     try:
#         url = 'https://akira-rest-api.herokuapp.com/getDecryptionData/{}/?format=json'.format(username)
#         response = requests.get(url)
#         dataUsername = response.json()
#     except Exception:
#         messages.info(request, "Server under maintenance. Please try again later.")
#         return redirect('login')

#     try:
#         get_attempt_ARU = UserLoginDetails.objects.get(
#                         id = userLoginObj,
#                         user__username = dataUsername['DecryptedUsername'], 
#                         attempt = "Manual Confirmation Required",
#                         reason = "Login is unusual",
#                         user_confirm = "Pending due to unusual login")
#     except UserLoginDetails.DoesNotExist:
#         get_attempt_ARU = None
#     if get_attempt_ARU:
#         get_attempt_ARU = UserLoginDetails.objects.get(
#                         id = userLoginObj,
#                         user__username = dataUsername['DecryptedUsername'], 
#                         attempt = "Manual Confirmation Required",
#                         reason = "Login is unusual",
#                         user_confirm = "Pending due to unusual login")
#         if get_attempt_ARU.user.username == dataUsername['DecryptedUsername']:
#             if user_response == "yes":
#                 get_attempt_ARU = UserLoginDetails.objects.filter(id = userLoginObj, user__username = dataUsername['DecryptedUsername'], attempt = "Manual Confirmation Required").order_by('-created_at')[0]
#                 get_attempt_ARU.attempt = "Success"
#                 get_attempt_ARU.user_confirm = "Login Confirmed"
#                 get_attempt_ARU.reason = "Login Confirmed via Email Manually"
#                 get_attempt_ARU.save()
#                 user = User.objects.get(username = dataUsername['DecryptedUsername'])
#                 user.is_active = True
#                 user.save()
#                 return HttpResponse(status=200)
#             else:
#                 logout(request)
#                 return HttpResponse(status=400)
#         else:
#             logout(request)
#             return HttpResponse(status=400)
#     else:
#         logout(request)
#         return HttpResponse(status=400)

# def checkUserResponse(request, username, userLoginObj):
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
#     try:
#         userLoginDetails = UserLoginDetails.objects.get(
#                         id = userLoginObj,
#                         user__username = dataUsername['DecryptedUsername'], 
#                         attempt = "Success",
#                         user_ip_address = ip,
#                         user_confirm = "Login Confirmed",
#                         reason = "Login Confirmed via Email Manually")
#     except UserLoginDetails.DoesNotExist:
#         userLoginDetails = None
#     if (userLoginDetails) and (userLoginDetails.user_ip_address == ip):
#         user = User.objects.get(username = dataUsername['DecryptedUsername'])
#         login(request, user)
#         userLoginDetails.sessionKey = request.session.session_key
#         userLoginDetails.score = getLoginScore(userLoginObj, dataUsername['DecryptedUsername'])
#         userLoginDetails.save()
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

    if User_IP_S_List.objects.filter(suspicious_list = ip).exists() is True:
        messages.warning(request, "We can't process your Switch Device request")
        return redirect('login')
    else:
        if request.method == 'POST':
            currentUsername = request.POST.get('username')
            try:
                captcha_token = request.POST.get("g-recaptcha-response")
                cap_url = "https://www.google.com/recaptcha/api/siteverify"
                cap_secret = settings.GOOGLE_RECAPTCHA_SECRET_KEY
                cap_data = {"secret": cap_secret, "response": captcha_token}
                cap_server_response = requests.post(url = cap_url, data = cap_data)
                cap_json = json.loads(cap_server_response.text)
            except Exception:
                messages.info(request, 'Check your internet connection')
                return redirect('requestSwitchDevice')
            if not cap_json['success'] is True:
                messages.info(request, "Invalid reCaptcha!")
                return redirect('requestSwitchDevice')
            else:
                try:
                    getUserObject = User.objects.get(username = currentUsername)
                except User.DoesNotExist:
                    messages.info(request, "Account doesn't exists!")
                    return redirect('requestSwitchDevice')
                try:
                    url = 'https://akira-rest-api.herokuapp.com/getEncryptionData/{}/?format=json'.format(currentUsername)
                    response = requests.get(url)
                    dataUsername = response.json()
                except Exception:
                    messages.info(request, "Server under maintenance. Please try again later.")
                    return redirect('requestSwitchDevice')

                ten_minutes_ago = pydt.datetime.now() + pydt.timedelta(minutes=-10)
                if SwitchDevice.objects.filter(user = getUserObject, reason = "Not Approved Yet", created_at__gte = ten_minutes_ago).exists() is True:
                    messages.info(request, "You have already requested to switch device!")
                    getReqSDObj = SwitchDevice.objects.get(user = getUserObject, userIPAddr = ip, reason = "Not Approved Yet")
                    if SwitchDevice.objects.filter(user = getUserObject, userIPAddr = ip, reason = "Not Approved Yet").exists() is True:
                        return redirect('waitingSwitchDeviceResponse', switchDeviceReqID = getReqSDObj.id, username = dataUsername['EncryptedUsername'])
                    else:
                        return redirect('requestSwitchDevice')
                # elif SwitchDevice.objects.filter(user = getUserObject, reason = "Not Approved Yet").exists() is True:
                #     SwitchDevice.objects.filter(user = getUserObject, reason = "Not Approved Yet").delete()
                #     switchDeviceObj = SwitchDevice.objects.create(
                #             userIPAddr = ip,
                #             userBrowser = browser,
                #             userOS = OS_Details,
                #             reason = "Not Approved Yet",
                #             user = getUserObject)
                #     switchDeviceID = SwitchDevice.objects.get(id = switchDeviceObj.id)
                #     return redirect('waitingSwitchDeviceResponse', switchDeviceReqID = switchDeviceID.id,  username = dataUsername['EncryptedUsername'])
                elif SwitchDevice.objects.filter(user = getUserObject, status = "Switch Device Successful").exists() is True:
                    messages.error(request, "Terminate the active session in order to make new Switch Device request")
                    return redirect('requestSwitchDevice')
                else:
                    switchDeviceObj = SwitchDevice.objects.create(
                            userIPAddr = ip,
                            userBrowser = browser,
                            userOS = OS_Details,
                            reason = "Not Approved Yet",
                            user = getUserObject)
                    switchDeviceID = SwitchDevice.objects.get(id = switchDeviceObj.id)
                    return redirect('waitingSwitchDeviceResponse', switchDeviceReqID = switchDeviceID.id,  username = dataUsername['EncryptedUsername'])
        context = {
            "GOOGLE_RECAPTCHA_PUBLIC_KEY": settings.GOOGLE_RECAPTCHA_PUBLIC_KEY,
        }
        return render(request, 'authentication/SwitchDevice/requestSwitchDevice.html', context)

def waitingSwitchDeviceResponse(request, switchDeviceReqID, username):
    try:
        checkSDAOT = SwitchDevice.objects.get(id = switchDeviceReqID)
    except SwitchDevice.DoesNotExist:
        messages.error(request, "Switch Device Request doesn't exists!")
        return redirect('requestSwitchDevice')
    
    if checkSDAOT:
        if checkSDAOT.status == "Terminated":
            messages.error(request, "Switch Device request is closed!")
            return redirect('requestSwitchDevice')

    context = {
        "currentUsername": username,
        "switchDeviceID": switchDeviceReqID,
    }
    return render(request, 'authentication/SwitchDevice/waitingSwitchDeviceResponse.html', context)

@login_required(login_url=settings.LOGIN_URL)
def validateSwitchDevice(request):
    getSwitchDeviceRequests = SwitchDevice.objects.filter(user = request.user).order_by('-created_at')
    try:
        currentSDReq = SwitchDevice.objects.get(user = request.user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending")
    except SwitchDevice.DoesNotExist:
        try:
            currentSDReq = SwitchDevice.objects.get(user = request.user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Pending")
        except SwitchDevice.DoesNotExist:
            try:
                currentSDReq = SwitchDevice.objects.get(user = request.user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Successful")
            except SwitchDevice.DoesNotExist:
                currentSDReq = None
    try:
        if request.session.session_key == currentSDReq.sessionKey:
            terminate_access = "Denied"
        else:
            terminate_access = "Allowed"
    except Exception:
        terminate_access = "NA"
    if request.method == "POST":
        if currentSDReq.user == request.user:
            try:
                getLastPage = UserPageVisits.objects.filter(user = request.user).order_by('-created_at')[0]
                pageURL = getLastPage.currentPage
            except Exception:
                getLastPage = None
                current_site = get_current_site(request)
                pageURL = "http://"+str(current_site.domain)+"/"
            update_currentSDReq = currentSDReq
            update_currentSDReq.userConfirm = "User Approved"
            update_currentSDReq.reason = "User Confirmed the Switch Device"
            update_currentSDReq.currentPage = pageURL
            update_currentSDReq.status = "Switch Device Pending"
            update_currentSDReq.save()
            user = User.objects.get(username = request.user.username)
            user.is_active = True
            user.save()
            messages.info(request, "Your approval request is been taken")
            return redirect('validateSwitchDevice')
        else:
            logout(request)
            return HttpResponse("No Switch Device Request Found!")
    context = {
        "currentSDReq": currentSDReq,
        "getSwitchDeviceRequests": getSwitchDeviceRequests,
        "terminate_access":terminate_access,
    }
    return render(request, 'authentication/SwitchDevice/acceptSwitchDevice.html', context)

@login_required(login_url=settings.LOGIN_URL)
def denySwitchDevice(request, switchDeviceReqID):
    update_currentSDReq = SwitchDevice.objects.get(id = switchDeviceReqID, user__username = request.user.username)
    update_currentSDReq.userConfirm = "User Denied"
    update_currentSDReq.reason = "User Denied the Switch Device"
    update_currentSDReq.status = "Terminated"
    update_currentSDReq.save()
    messages.info(request, "Your Denied Request is been taken successfully")
    return redirect('validateSwitchDevice')

@login_required(login_url=settings.LOGIN_URL)
def terminateSwitchDevice(request, switchDeviceReqID):
    update_currentSDReq = SwitchDevice.objects.get(id = switchDeviceReqID, user__username = request.user.username)
    if request.session.session_key == update_currentSDReq.sessionKey:
        messages.info(request, "You don't have access to terminate the session")
    else:
        try:
            session = Session.objects.get(session_key=update_currentSDReq.sessionKey)
            session.delete()
        except Exception:
            messages.info(request, "Session is already terminated")
        update_currentSDReq.status = "Terminated"
        update_currentSDReq.save()
        messages.info(request, "Your Terminate Request is been taken successfully")
    return redirect('validateSwitchDevice')

def checkValidatedSwitchDeviceRequest(request, username, switchDeviceID):
    try:
        currentSDObj = SwitchDevice.objects.get(id=switchDeviceID)
    except SwitchDevice.DoesNotExist:
        currentSDObj = None

    getCurrentSDReqOvertimeObj = False
    try:
        getCurrentSDReqOvertime = SwitchDevice.objects.get(id=switchDeviceID)
        eleven_minutes = getCurrentSDReqOvertime.created_at + pydt.timedelta(minutes=+11)
    except Exception:
        getCurrentSDReqOvertime = None
    if (getCurrentSDReqOvertime) and (pydt.datetime.now() >= eleven_minutes):
        getCurrentSDReqOvertime.delete()
        getCurrentSDReqOvertimeObj = True

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
        GetSwitchDeviceRequestObjectUD = SwitchDevice.objects.get(
                        id = switchDeviceID,
                        user__username=dataUsername['DecryptedUsername'],
                        status = "Terminated")
    except SwitchDevice.DoesNotExist:
        GetSwitchDeviceRequestObjectUD = None

    try:
        getCurrentSDReq = SwitchDevice.objects.get(
                        id = switchDeviceID,
                        user__username=dataUsername['DecryptedUsername'], 
                        userConfirm = "User Approved",
                        reason = "User Confirmed the Switch Device",
                        status = "Switch Device Pending")
    except SwitchDevice.DoesNotExist:
        getCurrentSDReq = None

    if (getCurrentSDReq) and (getCurrentSDReq.userIPAddr == ip):
        user = User.objects.get(username = dataUsername['DecryptedUsername'])
        currentUrl = getCurrentSDReq.currentPage
        login(request, user)
        getCurrentSDReq.sessionKey = request.session.session_key
        getCurrentSDReq.save()
        data = {
            'status': 'success',
            'redirect_url': currentUrl,
        }
    elif (GetSwitchDeviceRequestObjectUD) and (GetSwitchDeviceRequestObjectUD.userIPAddr == ip):
        data = {
            'status': 'failed',
            'message': 'User Denied',
        }
    elif currentSDObj is None:
        data = {
            'status': 'failed',
            'message': 'Object does not exist',
        }
    elif getCurrentSDReqOvertimeObj is True:
        data = {
            'status': 'failed',
            'message': 'Request Expired',
        }
    else:
        data = {
            'status': 'failed',
        }
    response = JsonResponse(data)
    return response

def SwitchDeviceStatus(request, username):
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
        getCurrentSDReq = SwitchDevice.objects.get(
                        user__username = dataUsername['DecryptedUsername'], 
                        userConfirm = "User Approved",
                        reason = "User Confirmed the Switch Device",
                        status = "Switch Device Pending")
    except SwitchDevice.DoesNotExist:
        getCurrentSDReq = None
    if (getCurrentSDReq) and (getCurrentSDReq.userIPAddr == ip):
        updateCurrentSDReq = getCurrentSDReq
        updateCurrentSDReq.userIPAddr = ip
        updateCurrentSDReq.status = "Switch Device Successful"
        updateCurrentSDReq.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse("No Switch Device Request Found!")

@login_required(login_url=settings.LOGIN_URL)
def SyncDevice(request, switchDeviceID):
    try:
        getCurrentSDReq = SwitchDevice.objects.get(id = switchDeviceID, status = "Terminated")
    except SwitchDevice.DoesNotExist:
        getCurrentSDReq = None
    if getCurrentSDReq == None:
        getSecondDevice = SwitchDevice.objects.filter(
                                user = request.user,
                                userConfirm = "User Approved",
                                status = "Switch Device Successful",
                                reason = "User Confirmed the Switch Device").order_by('-created_at')[0]
        getSecondDeviceCurrentPage = UserPageVisits.objects.filter(
                                    user = request.user,
                                    userIPAddr = getSecondDevice.userIPAddr).order_by('-created_at')[0]
        return redirect(getSecondDeviceCurrentPage.currentPage)
    else:
        messages.error(request, "Switch Device is terminated")
        return redirect('validateSwitchDevice')

def UsernameEncryptedCookie(request, username):
    username10 = len(username) * 10
    username_hex = username.encode('utf-8').hex()

    n = username10
    ranString = ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    ranStringList = []
    for i in range(0,len(username)):
        ranStringList.append(ranString[i*10:(i+1)*10])

    ranDigits = [random.randint(1, 6) for i in range(len(username))]

    for i in range(0,len(username)):
        ranStringList[i] = ranStringList[i][:ranDigits[i]] + username_hex[i*2:i*2+2] + ranStringList[i][ranDigits[i]+2:]

    saltArrayAT = ranStringList
    SecLarAUS = -2
    random_digit = ranDigits
    for i in range(0,len(username)):
        saltArrayAT[i] = saltArrayAT[i][:SecLarAUS] + str(random_digit[i]) + saltArrayAT[i][SecLarAUS+1:]

    ranStringList_str = "".join(ranStringList)
    return ranStringList_str

def logoutUser(request):
    currentSDUAUCSDSDS = SwitchDevice.objects.filter(user = request.user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Successful").exists()
    currentSDPNA = SwitchDevice.objects.filter(user = request.user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending").exists()
    
    logoutResponse = render(request, 'authentication/login.html')

    ranKey = UsernameEncryptedCookie(request, request.user.username)
    cookie_max_age = 604800
    expire_time = pydt.datetime.strftime(pydt.datetime.utcnow() + pydt.timedelta(seconds=cookie_max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    
    logoutResponse.set_cookie(key='access_token', value=ranKey, max_age=cookie_max_age, expires=expire_time)
    
    if (request.user.is_authenticated) and (TwoFactorAuth.objects.filter(user = request.user, twofa = False).exists() is True):
        UserPageVisits.objects.filter(user = request.user).delete()
        if currentSDUAUCSDSDS is True:
            updatecurrentSDUAUCSDSDS = SwitchDevice.objects.get(user = request.user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Successful")
            updatecurrentSDUAUCSDSDS.reason = "User Logged Out"
            updatecurrentSDUAUCSDSDS.status = "Terminated"
            updatecurrentSDUAUCSDSDS.save()
        if currentSDPNA is True:
            updatecurrentSDPNA = SwitchDevice.objects.get(user = request.user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending")
            updatecurrentSDPNA.userConfirm = "User Denied"
            updatecurrentSDPNA.reason = "User Logged Out"
            updatecurrentSDPNA.status = "Terminated"
            updatecurrentSDPNA.save()

        currentULObj = UserLoginDetails.objects.get(user__username = request.user.username, sessionKey = request.session.session_key)
        currentULObj.Logoutcookie = ranKey
        currentULObj.save()
        logout(request)
        return logoutResponse
    elif (request.user.is_authenticated) and (TwoFactorAuth.objects.filter(user = request.user, twofa = True).exists() is True):
        UserPageVisits.objects.filter(user = request.user).delete()
        if currentSDUAUCSDSDS is True:
            updatecurrentSDUAUCSDSDS = SwitchDevice.objects.get(user = request.user, userConfirm = "User Approved", reason = "User Confirmed the Switch Device", status = "Switch Device Successful")
            updatecurrentSDUAUCSDSDS.reason = "User Logged Out"
            updatecurrentSDUAUCSDSDS.status = "Terminated"
            updatecurrentSDUAUCSDSDS.save()
        if currentSDPNA is True:
            updatecurrentSDPNA = SwitchDevice.objects.get(user = request.user, userConfirm = "Pending", reason = "Not Approved Yet", status = "Switch Device Pending")
            updatecurrentSDPNA.userConfirm = "User Denied"
            updatecurrentSDPNA.reason = "User Logged Out"
            updatecurrentSDPNA.status = "Terminated"
            updatecurrentSDPNA.save()
        try:
            UBC = User_BackUp_Codes.objects.get(user = request.user)
            if UBC.download == False:
                messages.info(request, "Please Download Backup codes")
                return redirect('account_settings')
            else:
                currentULObj = UserLoginDetails.objects.get(user__username = request.user.username, sessionKey = request.session.session_key)
                currentULObj.Logoutcookie = ranKey
                currentULObj.save()
                logout(request)
                return logoutResponse
        except User_BackUp_Codes.DoesNotExist:
            messages.info(request, "Please generate Backup codes")
            return redirect('account_settings')
    elif (request.user.is_authenticated):
        currentULObj = UserLoginDetails.objects.get(user__username = request.user.username, sessionKey = request.session.session_key)
        currentULObj.Logoutcookie = ranKey
        currentULObj.save()
        logout(request)
        return logoutResponse
    else:
        return logoutResponse

# # Encrypting the cookie with content username
# username = "4akhi"
# print("Username",username)
# username10 = len(username) * 10

# # convert username into hex
# username_hex = username.encode('utf-8').hex()
# print("Username HEX",username_hex)

# n = username10
# ranString = ''.join(random.choices(string.ascii_letters + string.digits, k=n))
# print("Random String",ranString)

# # Divide the ranString by length of username and store it in a list
# ranStringList = []
# for i in range(0,len(username)):
#     ranStringList.append(ranString[i*10:(i+1)*10])
# print("Divide", ranStringList)

# # Generate n random numbers between 1 and 6
# ranDigits = [random.randint(1, 6) for i in range(len(username))]
# # ranDigits = "".join(str(i) for i in ranDigits)
# print("N Random Number ",ranDigits)

# # Replace the two characters in each element of ranStringList at the index of ranDigits with the two characters in username_hex
# for i in range(0,len(username)):
#     ranStringList[i] = ranStringList[i][:ranDigits[i]] + username_hex[i*2:i*2+2] + ranStringList[i][ranDigits[i]+2:]
# print("Username HEX Replaced ", ranStringList)


# saltArrayAT = ranStringList
# SecLarAUS = -2
# random_digit = ranDigits
# # Replace the characters in each element of saltArrayAT using SecLarAUS value as Index from the last with characters of random_digit
# for i in range(0,len(username)):
#     saltArrayAT[i] = saltArrayAT[i][:SecLarAUS] + str(random_digit[i]) + saltArrayAT[i][SecLarAUS+1:]
# print("Random Digit Replaced ", saltArrayAT)

# # Convert the ranStringList into a string
# ranStringList_str = "".join(ranStringList)
# print("ranStringList str", ranStringList_str)

# # Decrypting the Encrypting the cookie with content username
# username = "4akhilkumar"
# EncryptedCookie = "pumP349u4KVem61ZcA37f6bxpg7q1H2bqdc68W58W48Go69S56r7X6cB9n3NRKhrzE6b6JORDaev756G3g0ezr6d6wyVj4Tk616PsNX672YH4U"

# username10 = len(username) * 10

# # Divide the EncryptedCookie by length of username and store it in a list
# EncryptedCookieList = []
# for i in range(0,len(username)):
#     EncryptedCookieList.append(EncryptedCookie[i*10:(i+1)*10])
# print("Divide", EncryptedCookieList)
# # ['UmnqCu5hin', '5C7RfJf6Ev', 'Iz2n2hnBWc', 'Z1yb0JViCx', 'L4a8sXuBsq']

# # Find the random digits in the encryptedText_list
# randomDigits = []
# # Store the last nth character of each element in the encryptedText_list in randomDigits list
# for i in range(len(EncryptedCookieList)):
#     randomDigits.append(EncryptedCookieList[i][-2])
# print("Random Digits",randomDigits)
# # N Random Number  [3, 1, 6, 2, 3]

# # get the elements of the encryptedText_list at specific index using randomDigits elements as index values and store it in a list name final_list
# HexList = []
# for i in range(len(EncryptedCookieList)):
#     HexList.append(EncryptedCookieList[i][int(randomDigits[i])]+EncryptedCookieList[i][int(randomDigits[i])+1])
# print(HexList)

# # Convert the HexList elements to ASCII and store it in a final_list
# final_list = []
# for i in range(len(HexList)):
#     final_list.append(chr(int(HexList[i], 16)))
# print(final_list)

# final_list_hex_str = "".join(final_list)
# print(final_list_hex_str)