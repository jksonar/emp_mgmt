from django.contrib import admin
from .models import Attendance, AttendanceCorrection
# Register your models here.
admin.site.register(Attendance)
admin.site.register(AttendanceCorrection)  
