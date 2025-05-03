from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Attendance URLs
    path('', views.attendance_list, name='attendance_list'),
    path('mark/', views.attendance_mark, name='attendance_mark'),
    path('<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('<int:pk>/update/', views.attendance_update, name='attendance_update'),
    
    # Attendance Correction URLs
    path('corrections/', views.correction_list, name='correction_list'),
    path('corrections/create/', views.correction_create, name='correction_create'),
    path('corrections/<int:pk>/', views.correction_detail, name='correction_detail'),
    path('corrections/<int:pk>/approve/', views.correction_approve, name='correction_approve'),
    
    # Attendance Reports
    path('reports/daily/', views.daily_report, name='daily_report'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/employee/', views.employee_report, name='employee_report'),
] 