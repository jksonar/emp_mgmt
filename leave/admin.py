from django.contrib import admin
from .models import LeaveType, LeaveApplication, LeaveBalance
# Register your models here.
admin.site.register(LeaveType)
admin.site.register(LeaveApplication)
admin.site.register(LeaveBalance)
