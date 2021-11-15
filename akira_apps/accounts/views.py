from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import re
import secrets
import datetime as pydt
import datetime

from akira_apps.accounts.models import TwoFactorAuth
from akira_apps.authentication.models import User_BackUp_Codes, UserLoginDetails

# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def account_settings(request):
    username = request.user 
    status_2fa = TwoFactorAuth.objects.filter(user=username)
    try:
        backup_codes = User_BackUp_Codes.objects.get(user=username)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes == None:
        backup_codes_status = 0
    else:
        backup_codes_status = 1

    try:
        status_2fa = TwoFactorAuth.objects.get(user=username)
    except TwoFactorAuth.DoesNotExist:
        status_2fa = None
    current_user_2fa_status = 0
    if (status_2fa != None) and (status_2fa.twofa == 0):
        current_user_2fa_status = 0
    elif (status_2fa != None) and (status_2fa.twofa == 1):
        current_user_2fa_status = 1
    else:
        current_user_2fa_status = 0

    start_month = pydt.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nxt_mnth = start_month.replace(day=28) + datetime.timedelta(days=4)
    res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    end_month = pydt.datetime.now().replace(day=res.day, hour=0, minute=0, second=0, microsecond=0)

    get_success_attempt = UserLoginDetails.objects.filter(user = username, attempt = 'Success', created_at__range=(start_month,end_month))

    def ordinal(n):
        s = ('th', 'st', 'nd', 'rd') + ('th',)*10
        v = n%100
        if v > 13:
            return f'{n}{s[v%10]}'
        else:
            return f'{n}{s[v]}'

    get_dates = []
    for i in get_success_attempt:
        get_dates.append(i.created_at.strftime("%d"))
    
    removed_duplicate_date = list(sorted(set(get_dates)))

    month = pydt.datetime.now().strftime(" %b")
    current_month = pydt.datetime.now().strftime(" %B")
    remove_duplicate_date_after_ordinal = []
    for i in removed_duplicate_date:
        remove_duplicate_date_after_ordinal.append(str(ordinal(int(i))) + month)

    success_attempts_date = []
    for i in removed_duplicate_date:
        start_date = pydt.datetime.now().replace(day=int(i), hour=0, minute=0, second=0, microsecond=0)
        end_date = pydt.datetime.now().replace(day=int(i), hour=23, minute=59, second=59, microsecond=0)
        attempt_on_that_date = UserLoginDetails.objects.filter(user__username = username, attempt = 'Success', created_at__range=(start_date,end_date)).count()
        success_attempts_date.append(attempt_on_that_date)
    
    failed_attempts_date = []
    for i in removed_duplicate_date:
        start_date = pydt.datetime.now().replace(day=int(i), hour=0, minute=0, second=0, microsecond=0)
        end_date = pydt.datetime.now().replace(day=int(i), hour=23, minute=59, second=59, microsecond=0)
        attempt_on_that_date = UserLoginDetails.objects.filter(user__username = username, attempt = 'Failed', created_at__range=(start_date,end_date)).count()
        failed_attempts_date.append(attempt_on_that_date)

    get_failed_login_attempts = UserLoginDetails.objects.filter(user__username = username, attempt = 'Failed')
    get_failed_attempt_in_a_month = UserLoginDetails.objects.filter(user = username, attempt = 'Failed', created_at__range=(start_month,end_month)).count()
    get_failed_login_attempts_count = UserLoginDetails.objects.filter(user__username = username, attempt = 'Failed').count()
        
    context = {
        "backup_codes_status":backup_codes_status,
        "current_user_2fa_status":current_user_2fa_status,
        "current_month":current_month,
        "get_dates":remove_duplicate_date_after_ordinal,
        "success_attempts_date":success_attempts_date,
        "failed_attempts_date":failed_attempts_date,
        "get_failed_login_attempts":get_failed_login_attempts,
        "get_failed_attempt_in_a_month":get_failed_attempt_in_a_month,
        "get_failed_login_attempts_count":get_failed_login_attempts_count,
    }
    return render(request, 'accounts/manage_account.html', context)

@login_required(login_url=settings.LOGIN_URL)
def generate_backup_codes(request):
    username = request.user
    try:
        status_2fa = TwoFactorAuth.objects.get(user=username)
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
        backup_codes = User_BackUp_Codes.objects.get(user=username)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if current_user_2fa_status == 1:
        if backup_codes == None:
            list_codes = secrets.token_urlsafe(45)
            split_str = re.findall('.{1,6}', str(list_codes))
            join_hash = '#'.join(split_str)
            userbackupcodes = User_BackUp_Codes(user = username,backup_codes = join_hash)
            userbackupcodes.save()
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
    username = request.user
    try:
        backup_codes = User_BackUp_Codes.objects.get(user=username)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes != None:
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=BackUp Codes - ' + str(username) + ' - AkirA Account' + '.txt'
        current_user_backup_codes = User_BackUp_Codes.objects.get(user=username)
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
    username = request.user
    try:
        backup_codes = User_BackUp_Codes.objects.get(user=username)
    except User_BackUp_Codes.DoesNotExist:
        backup_codes = None
    if backup_codes == None:
        messages.info(request, "No Backup codes to delete")
        return redirect('account_settings')
    else:
        backup_codes = User_BackUp_Codes.objects.get(user=username)
        backup_codes.delete()
        messages.info(request, "Backup codes deleted")
    return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def status_2fa(request):
    current_user = request.user
    try:
        check_current_user_2fa = TwoFactorAuth.objects.get(user=current_user)
    except TwoFactorAuth.DoesNotExist:
        check_current_user_2fa = None
    if check_current_user_2fa == None:
        create_enable_2fa = TwoFactorAuth.objects.create(user=current_user, twofa = 1)
        create_enable_2fa.save()
        messages.info(request, "2-Factor Authentication is enabled")
    else:
        check_current_user_2fa_status = TwoFactorAuth.objects.get(user=current_user)
        if check_current_user_2fa_status.twofa == False:
            update_enable_2fa = TwoFactorAuth.objects.get(id = check_current_user_2fa_status.id)
            update_enable_2fa.twofa = 1
            update_enable_2fa.save()
            messages.info(request, "2-Factor Authentication is enabled")
        else:
            update_disable_2fa = TwoFactorAuth.objects.get(id = check_current_user_2fa_status.id)
            update_disable_2fa.twofa = 0
            update_disable_2fa.save()
            messages.info(request, "2-Factor Authentication is disabled")
            return redirect('delete_existing_backup_codes')
    return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def agree_login_attempt(request, login_attempt_id):
    current_user = request.user
    update_login_confirm = UserLoginDetails.objects.get(id=login_attempt_id)
    if current_user == update_login_confirm.user:
        update_login_confirm.user_confirm = "YES"
        update_login_confirm.save()
        messages.success(request, "Login Activity Confirmed!")
        return redirect('account_settings')
    else:
        messages.warning(request, "Access Denied!")
        return redirect('account_settings')

@login_required(login_url=settings.LOGIN_URL)
def deny_login_attempt(request, login_attempt_id):
    current_user = request.user
    update_login_confirm = UserLoginDetails.objects.get(id=login_attempt_id)
    if current_user == update_login_confirm.user:
        update_login_confirm.user_confirm = "NO"
        update_login_confirm.save()
        messages.success(request, "Login Activity Confirmed!")
        return redirect('account_settings')
    else:
        messages.warning(request, "Access Denied!")
        return redirect('account_settings')

# backUpCode = TwoFactorAuth.objects.all()
# TwoFactorAuth.objects.all().delete()
# backUpCode = TwoFactorAuth.objects.all()
# print(backUpCode)

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