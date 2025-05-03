from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Salary Structure URLs
    path('structures/', views.salary_structure_list, name='salary_structure_list'),
    path('structures/create/', views.salary_structure_create, name='salary_structure_create'),
    path('structures/<int:pk>/', views.salary_structure_detail, name='salary_structure_detail'),
    path('structures/<int:pk>/update/', views.salary_structure_update, name='salary_structure_update'),
    
    # Payroll URLs
    path('', views.payroll_list, name='payroll_list'),
    path('create/', views.payroll_create, name='payroll_create'),
    path('<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('<int:pk>/update/', views.payroll_update, name='payroll_update'),
    path('<int:pk>/approve/', views.payroll_approve, name='payroll_approve'),
    path('<int:pk>/payslip/', views.payslip_generate, name='payslip_generate'),
    
    # Payroll Reports
    path('reports/monthly/', views.monthly_payroll_report, name='monthly_payroll_report'),
    path('reports/employee/', views.employee_payroll_report, name='employee_payroll_report'),
] 