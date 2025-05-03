from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Salary Structure URLs
    path('structures/', views.SalaryStructureListView.as_view(), name='salary_structure_list'),
    path('structures/create/', views.SalaryStructureCreateView.as_view(), name='salary_structure_create'),
    path('structures/<int:pk>/', views.SalaryStructureDetailView.as_view(), name='salary_structure_detail'),
    path('structures/<int:pk>/update/', views.SalaryStructureUpdateView.as_view(), name='salary_structure_update'),
    path('structures/<int:pk>/delete/', views.SalaryStructureDeleteView.as_view(), name='salary_structure_delete'),
    
    # Payroll URLs
    path('', views.PayrollListView.as_view(), name='payroll_list'),
    path('create/', views.PayrollCreateView.as_view(), name='payroll_create'),
    path('<int:pk>/', views.PayrollDetailView.as_view(), name='payroll_detail'),
    path('<int:pk>/update/', views.PayrollUpdateView.as_view(), name='payroll_update'),
    path('<int:pk>/delete/', views.PayrollDeleteView.as_view(), name='payroll_delete'),
    path('<int:pk>/approve/', views.approve_payroll, name='payroll_approve'),
    path('<int:pk>/generate-payslip/', views.generate_payslip, name='generate_payslip'),
    path('payslips/<int:pk>/download/', views.download_payslip, name='download_payslip'),
    
    # Reports
    path('reports/monthly/', views.monthly_payroll_report, name='monthly_report'),
    path('reports/employee/', views.employee_payroll_report, name='employee_report'),
] 