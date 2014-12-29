from django.contrib import admin
from ccc_friend_schedule.models import Attendance

admin_site = admin.AdminSite()
admin_site.register(Attendance)