from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Management
    path('', views.CustomUserListView.as_view(), name='user_list'),
    path('create/', views.CustomUserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', views.CustomUserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', views.CustomUserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.CustomUserDeleteView.as_view(), name='user_delete'),
    
    # Profile Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Document Management
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    
    # Work History Management
    path('work-history/', views.work_history_list, name='work_history_list'),
    path('work-history/create/', views.work_history_create, name='work_history_create'),
    path('work-history/<int:pk>/update/', views.work_history_update, name='work_history_update'),
    path('work-history/<int:pk>/delete/', views.work_history_delete, name='work_history_delete'),
] 