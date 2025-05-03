from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    # Leave Types
    path('types/', views.LeaveTypeListView.as_view(), name='type_list'),
    path('types/create/', views.LeaveTypeCreateView.as_view(), name='type_create'),
    path('types/<int:pk>/', views.LeaveTypeDetailView.as_view(), name='type_detail'),
    path('types/<int:pk>/update/', views.LeaveTypeUpdateView.as_view(), name='type_update'),
    path('types/<int:pk>/delete/', views.LeaveTypeDeleteView.as_view(), name='type_delete'),
    
    # Leave Applications
    path('applications/', views.LeaveApplicationListView.as_view(), name='application_list'),
    path('applications/create/', views.LeaveApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', views.LeaveApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/update/', views.LeaveApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/delete/', views.LeaveApplicationDeleteView.as_view(), name='application_delete'),
    path('applications/<int:pk>/approve/', views.approve_leave, name='approve_leave'),
    path('applications/<int:pk>/reject/', views.reject_leave, name='reject_leave'),
    path('applications/<int:pk>/cancel/', views.cancel_leave, name='cancel_leave'),
    
    # Leave Balances
    path('balances/', views.LeaveBalanceListView.as_view(), name='balance_list'),
    path('balances/<int:pk>/', views.LeaveBalanceDetailView.as_view(), name='balance_detail'),
    path('balances/<int:pk>/update/', views.LeaveBalanceUpdateView.as_view(), name='balance_update'),
    
    # Reports
    path('reports/summary/', views.LeaveSummaryReportView.as_view(), name='summary_report'),
    path('reports/export/', views.export_leave_report, name='export_report'),
    
    # Pending Applications
    path('pending/', views.PendingLeaveListView.as_view(), name='pending_list'),
] 