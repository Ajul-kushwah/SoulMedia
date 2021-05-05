from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(WhoProfileView)
admin.site.register(UserOTP)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)