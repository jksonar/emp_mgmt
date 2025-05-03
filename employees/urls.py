from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'employees'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='employees/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='employees/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='employees/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='employees/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='employees/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='employees/password_reset_complete.html'), name='password_reset_complete'),
        
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