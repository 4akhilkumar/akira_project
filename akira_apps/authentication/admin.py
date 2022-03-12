from django.contrib import admin
from .models import (UserLoginDetails, User_BackUp_Codes, 
                    User_BackUp_Codes_Login_Attempts, SwitchDevice, 
                    User_IP_List, UserPageVisits)

admin.site.register(UserLoginDetails)
admin.site.register(User_IP_List)
admin.site.register(User_BackUp_Codes)
admin.site.register(User_BackUp_Codes_Login_Attempts)
admin.site.register(SwitchDevice)
admin.site.register(UserPageVisits)