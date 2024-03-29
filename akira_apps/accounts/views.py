from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import re
import secrets
import datetime as pydt
import datetime

from akira_apps.accounts.models import (TwoFactorAuth)
from akira_apps.authentication.models import (User_BackUp_Codes, User_IP_List, UserLoginDetails)
from akira_apps.adops.models import (UserProfile)

def ordinal(n):
    s = ('th', 'st', 'nd', 'rd') + ('th',)*10
    v = n%100
    if v > 13:
        return f'{n}{s[v%10]}'
    else:
        return f'{n}{s[v]}'

@login_required(login_url=settings.LOGIN_URL)
def fetchLoginDetailsAjax(request):
    if request.method == 'POST':
        date = 1
        # get current year using datetime module
        year = pydt.datetime.now().year
        month = int(request.POST.get('request_month'))

        req_month = pydt.datetime(year, month, date)

        start_month = req_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        nxt_mnth = start_month.replace(day=28) + datetime.timedelta(days=4)
        res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
        end_month = req_month.replace(day=res.day, hour=23, minute=59, second=59, microsecond=0)

        get_attempt = UserLoginDetails.objects.filter(user__username = request.user.username, created_at__range=(start_month,end_month))

        get_dates = []
        for i in get_attempt:
            get_dates.append(i.created_at.strftime("%d"))
        
        removed_duplicate_date = list(sorted(set(get_dates)))

        month = req_month.strftime(" %b")
        remove_duplicate_date_after_ordinal = []
        for i in removed_duplicate_date:
            remove_duplicate_date_after_ordinal.append(str(ordinal(int(i))) + month)

        success_attempts_date = []
        for i in removed_duplicate_date:
            start_date = req_month.replace(day=int(i), hour=0, minute=0, second=0, microsecond=0)
            end_date = req_month.replace(day=int(i), hour=23, minute=59, second=59, microsecond=0)
            attempt_on_that_date = UserLoginDetails.objects.filter(user__username = request.user.username, attempt = 'Success', created_at__range=(start_date,end_date)).count()
            success_attempts_date.append(attempt_on_that_date)
        
        failed_attempts_date = []
        for i in removed_duplicate_date:
            start_date = req_month.replace(day=int(i), hour=0, minute=0, second=0, microsecond=0)
            end_date = req_month.replace(day=int(i), hour=23, minute=59, second=59, microsecond=0)
            attempt_on_that_date = UserLoginDetails.objects.filter(user__username = request.user.username, attempt = 'Failed', created_at__range=(start_date,end_date)).count()
            failed_attempts_date.append(attempt_on_that_date)

        return JsonResponse({
            "get_dates": remove_duplicate_date_after_ordinal,
            "success_attempts_date": success_attempts_date,
            "failed_attempts_date": failed_attempts_date,
        })

@login_required(login_url=settings.LOGIN_URL)
def account_settings(request):
    if TwoFactorAuth.objects.filter(user__username = request.user.username, twofa = True).exists() is True:
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0

    if UserProfile.objects.filter(user = request.user).exists() is True:
        current_user_details = UserProfile.objects.get(user = request.user)
    else:
        current_user_details = None

    try:
        backup_codes = User_BackUp_Codes.objects.get(user = request.user)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes == None:
        backup_codes_status = 0
    else:
        checkBackupCodesLength = len(backup_codes.backup_codes)
        if checkBackupCodesLength != 0:
            backup_codes_status = 1

    start_month = pydt.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nxt_mnth = start_month.replace(day=28) + datetime.timedelta(days=4)
    res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    end_month = pydt.datetime.now().replace(day=res.day, hour=23, minute=59, second=59, microsecond=0)

    get_unconfirmed_login_attempts = UserLoginDetails.objects.filter(Q(user__username = request.user.username, attempt = "Not Confirmed Yet!") | Q(user__username = request.user.username, attempt = "Need to verify")).order_by('-created_at')
    
    get_failed_attempt_in_a_month = UserLoginDetails.objects.filter(user = request.user, attempt = "Failed", user_confirm = 'Pending', score__lte = 15, created_at__range=(start_month,end_month)).count()
    try:
        get_currentLoginInfo = UserLoginDetails.objects.get(user__username = request.user.username, sessionKey = request.session.session_key)
    except Exception as e:
        get_currentLoginInfo = None
    thisDeviceCurrent = False

    if get_currentLoginInfo != None:
        try:
            getU53R_876_10 = request.COOKIES['U53R_876_10']
        except Exception:
            getU53R_876_10 = None
        if str(get_currentLoginInfo.bfp) == str(getU53R_876_10):
            thisDeviceCurrent = True

    context = {
        "current_user_details":current_user_details,
        "backup_codes_status":backup_codes_status,
        "current_user_2fa_status":current_user_2fa_status,
        "get_unconfirmed_login_attempts":get_unconfirmed_login_attempts,
        "get_failed_attempt_in_a_month":get_failed_attempt_in_a_month,
        "get_currentLoginInfo":get_currentLoginInfo,
        "thisDeviceCurrent":thisDeviceCurrent,
    }
    return render(request, 'accounts/manage_account.html', context)

@login_required(login_url=settings.LOGIN_URL)
def generate_backup_codes(request):
    if TwoFactorAuth.objects.filter(user = request.user, twofa = True).exists() is True:
        try:
            backup_codes = User_BackUp_Codes.objects.get(user=request.user)
        except User_BackUp_Codes.DoesNotExist:
            backup_codes = None
        if backup_codes == None:
            list_codes = secrets.token_urlsafe(45)
            split_str = re.findall('.{1,6}', str(list_codes))
            join_hash = '#'.join(split_str)
            User_BackUp_Codes.objects.create(user = request.user, backup_codes = join_hash)
            messages.success(request, "Backup Codes generated")
            return redirect('account_settings')
        else:
            messages.info(request, "Already Backup Codes Exists")
            return redirect('account_settings')
    else:
        messages.info(request, "You have to enable 2FA to generate Backup Codes")
        return redirect('account_settings')
    
@login_required(login_url=settings.LOGIN_URL)
def download_backup_codes(request):
    try:
        backup_codes = User_BackUp_Codes.objects.get(user=request.user)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes:
        updateBCDS = User_BackUp_Codes.objects.get(user=request.user)
        updateBCDS.download = True
        updateBCDS.save()
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=BackUp Codes - ' + str(request.user) + ' - AkirA Account' + '.txt'
        current_user_backup_codes = User_BackUp_Codes.objects.get(user=request.user)
        backup_codes_with_hash = current_user_backup_codes.backup_codes
        splitup_backup_codes = backup_codes_with_hash.split('#')
        align_backup_code = []
        for i in splitup_backup_codes:
            align_backup_code.append(f'{i}\n')
        response.writelines(align_backup_code)
        return response
    else:
        messages.info(request, "No Backup codes to download")
        return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def delete_existing_backup_codes(request):
    try:
        backup_codes = User_BackUp_Codes.objects.get(user=request.user)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes == None:
        messages.info(request, "No Backup codes to delete")
    else:
        backup_codes = User_BackUp_Codes.objects.get(user=request.user)
        backup_codes.delete()
        messages.info(request, "Backup codes deleted")
    return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def status_2fa(request):
    try:
        check_current_user_2fa = TwoFactorAuth.objects.get(user=request.user)
    except TwoFactorAuth.DoesNotExist:
        check_current_user_2fa = None
    if check_current_user_2fa == None:
        TwoFactorAuth.objects.create(user=request.user, twofa = True)
        messages.info(request, "2-Factor Authentication is enabled")
    else:
        check_current_user_2fa_status = TwoFactorAuth.objects.get(user=request.user)
        if check_current_user_2fa_status.twofa == False:
            update_enable_2fa = TwoFactorAuth.objects.get(id = check_current_user_2fa_status.id)
            update_enable_2fa.twofa = True
            update_enable_2fa.save()
            messages.info(request, "2-Factor Authentication is enabled")
        else:
            update_disable_2fa = TwoFactorAuth.objects.get(id = check_current_user_2fa_status.id)
            update_disable_2fa.twofa = False
            update_disable_2fa.save()
            messages.info(request, "2-Factor Authentication is disabled")
            return redirect('delete_existing_backup_codes')
    return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def agree_login_attempt(request, login_attempt_id):
    update_login_confirm = UserLoginDetails.objects.get(id=login_attempt_id)
    if request.user == update_login_confirm.user:
        update_login_confirm.user_confirm = "Login Confirmed"
        update_login_confirm.reason = "Login attempt confirmed via user manually"
        update_login_confirm.save()
        messages.success(request, "Login Activity Confirmed!")
        return redirect('account_settings')
    else:
        messages.warning(request, "Access Denied!")
        return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def deny_login_attempt(request, login_attempt_id):
    update_login_confirm = UserLoginDetails.objects.get(id=login_attempt_id)
    spam_ip_address = update_login_confirm.user_ip_address
    if request.user == update_login_confirm.user:
        update_login_confirm.user_confirm = "User Denied"
        update_login_confirm.reason = "Login attempt confirmed via user manually"
        update_login_confirm.save()
        messages.success(request, "Login Activity Confirmed!")
        User_IP_List.objects.create(suspicious_list=spam_ip_address)
        return redirect('account_settings')
    else:
        messages.warning(request, "Access Denied!")
        return redirect('account_settings')

# backUpCode = TwoFactorAuth.objects.all()
# User_IP_S_List.objects.all().delete()
# backUpCode = User_IP_S_List.objects.all()
# print(backUpCode)

# getUserLoginDetails = UserLoginDetails.objects.filter(user=None)
# getUserLoginDetails.delete()

# getUserLoginDetails = UserLoginDetails.objects.get(id="189a459b-8d2d-4cc0-bc3c-273a47fcf76a")
# getUserLoginDetails.delete()

# current_user = '4akhi'

# start_month = pydt.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# nxt_mnth = start_month.replace(day=28) + datetime.timedelta(days=4)
# res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
# end_month = pydt.datetime.now().replace(day=res.day, hour=0, minute=0, second=0, microsecond=0)

# get_failed_attempt = UserLoginDetails.objects.filter(user__username = current_user, attempt = 'Success', created_at__range=(start_month,end_month)).count()
# print("Failed Attempts",get_failed_attempt)
# print()
# get_success_attempt_count = UserLoginDetails.objects.filter(user__username = current_user, attempt = 'Success', created_at__range=(start_month,end_month)).count()
# print("Successful Attempts",get_success_attempt_count)

# get_success_attempt = UserLoginDetails.objects.filter(user__username = current_user, attempt = 'Success', created_at__range=(start_month,end_month))

# get_dates = []
# for i in get_success_attempt:
#     get_dates.append(i.created_at.strftime("%d"))
# removed_duplicate_date = list(sorted(set(get_dates)))

# attempts_date = []
# for i in removed_duplicate_date:
#     start_date = pydt.datetime.now().replace(day=int(i), hour=0, minute=0, second=0, microsecond=0)
#     end_date = pydt.datetime.now().replace(day=int(i), hour=23, minute=59, second=59, microsecond=0)
#     attempt_on_that_date = UserLoginDetails.objects.filter(user__username = current_user, attempt = 'Success', created_at__range=(start_date,end_date)).count()
#     attempts_date.append(attempt_on_that_date)
#     print("On date",i,"No.of attempts",attempt_on_that_date)
# print(attempts_date)