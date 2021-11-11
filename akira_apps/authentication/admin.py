from django.contrib import admin
from .models import UserLoginDetails, User_IP_B_List, UserVerificationStatus

admin.site.register(UserLoginDetails)
admin.site.register(User_IP_B_List)
admin.site.register(UserVerificationStatus)