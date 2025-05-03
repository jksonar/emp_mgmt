from django.contrib import admin

# Register your models here.
from .models import Payroll, SalaryComponent, SalaryStructure, SalaryStructureComponent, Payslip

admin.site.register(Payroll)
admin.site.register(SalaryComponent)
admin.site.register(SalaryStructure)
admin.site.register(SalaryStructureComponent)
admin.site.register(Payslip)


