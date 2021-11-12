from django.contrib import admin
from .models import UserLoginDetails, User_IP_B_List, UserVerificationStatus, User_BackUp_Codes, User_BackUp_Codes_Login_Attempts

admin.site.register(UserLoginDetails)
admin.site.register(User_IP_B_List)
admin.site.register(UserVerificationStatus)
admin.site.register(User_BackUp_Codes)
admin.site.register(User_BackUp_Codes_Login_Attempts)