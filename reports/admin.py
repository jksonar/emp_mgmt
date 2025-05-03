from django.contrib import admin
from .models import ReportTemplate, ReportSchedule, ReportExecution, Dashboard, DashboardWidget
# Register your models here.
admin.site.register(ReportTemplate)
admin.site.register(ReportSchedule)
admin.site.register(ReportExecution)
admin.site.register(Dashboard)
admin.site.register(DashboardWidget)


