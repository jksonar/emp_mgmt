from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    # Leave Type URLs
    path('types/', views.leave_type_list, name='leave_type_list'),
    path('types/create/', views.leave_type_create, name='leave_type_create'),
    path('types/<int:pk>/', views.leave_type_detail, name='leave_type_detail'),
    path('types/<int:pk>/update/', views.leave_type_update, name='leave_type_update'),
    path('types/<int:pk>/delete/', views.leave_type_delete, name='leave_type_delete'),
    
    # Leave Application URLs
    path('', views.leave_list, name='leave_list'),
    path('apply/', views.leave_apply, name='leave_apply'),
    path('<int:pk>/', views.leave_detail, name='leave_detail'),
    path('<int:pk>/update/', views.leave_update, name='leave_update'),
    path('<int:pk>/cancel/', views.leave_cancel, name='leave_cancel'),
    path('<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    
    # Leave Balance URLs
    path('balance/', views.leave_balance_list, name='leave_balance_list'),
    path('balance/<int:pk>/', views.leave_balance_detail, name='leave_balance_detail'),
] 