from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Employee Reports
    path('employees/', views.employee_directory, name='employee_directory'),
    path('employees/department/', views.department_employees, name='department_employees'),
    path('employees/attrition/', views.attrition_report, name='attrition_report'),
    
    # Attendance Reports
    path('attendance/daily/', views.attendance_daily_report, name='attendance_daily_report'),
    path('attendance/monthly/', views.attendance_monthly_report, name='attendance_monthly_report'),
    path('attendance/employee/', views.attendance_employee_report, name='attendance_employee_report'),
    
    # Leave Reports
    path('leave/balance/', views.leave_balance_report, name='leave_balance_report'),
    path('leave/usage/', views.leave_usage_report, name='leave_usage_report'),
    
    # Payroll Reports
    path('payroll/monthly/', views.payroll_monthly_report, name='payroll_monthly_report'),
    path('payroll/employee/', views.payroll_employee_report, name='payroll_employee_report'),
    
    # Performance Reports
    path('performance/reviews/', views.performance_review_report, name='performance_review_report'),
    path('performance/goals/', views.performance_goal_report, name='performance_goal_report'),
    
    # Export URLs
    path('export/employees/', views.export_employees, name='export_employees'),
    path('export/attendance/', views.export_attendance, name='export_attendance'),
    path('export/leave/', views.export_leave, name='export_leave'),
    path('export/payroll/', views.export_payroll, name='export_payroll'),
] 