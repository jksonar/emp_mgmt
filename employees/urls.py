from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.CustomUserListView.as_view(), name='user_list'),
    path('users/create/', views.CustomUserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.CustomUserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', views.CustomUserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.CustomUserDeleteView.as_view(), name='user_delete'),
    
    # Profile Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Document Management
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    
    # Employee Management
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Employee Documents
    path('<int:employee_id>/documents/', views.employee_document_list, name='employee_document_list'),
    path('<int:employee_id>/documents/upload/', views.employee_document_upload, name='employee_document_upload'),
    path('<int:employee_id>/documents/<int:pk>/', views.employee_document_detail, name='employee_document_detail'),
    path('<int:employee_id>/documents/<int:pk>/delete/', views.employee_document_delete, name='employee_document_delete'),
    
    # Work History
    path('<int:employee_id>/work-history/', views.work_history_list, name='work_history_list'),
    path('<int:employee_id>/work-history/create/', views.work_history_create, name='work_history_create'),
    path('<int:employee_id>/work-history/<int:pk>/update/', views.work_history_update, name='work_history_update'),
    path('<int:employee_id>/work-history/<int:pk>/delete/', views.work_history_delete, name='work_history_delete'),
] 