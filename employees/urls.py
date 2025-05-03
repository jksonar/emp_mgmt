from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee URLs
    path('', views.employee_list, name='employee_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Employee Profile URLs
    path('profile/', views.employee_profile, name='employee_profile'),
    path('profile/update/', views.employee_profile_update, name='employee_profile_update'),
    
    # Document URLs
    path('<int:employee_id>/documents/upload/', views.upload_document, name='upload_document'),
    path('documents/<int:document_id>/verify/', views.verify_document, name='verify_document'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    
    # Work History URLs
    path('<int:employee_id>/work-history/add/', views.add_work_history, name='add_work_history'),
    path('work-history/<int:work_history_id>/delete/', views.delete_work_history, name='delete_work_history'),
] 