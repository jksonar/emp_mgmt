from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    # Department URLs
    path('', views.department_list, name='department_list'),
    path('create/', views.department_create, name='department_create'),
    path('<int:pk>/', views.department_detail, name='department_detail'),
    path('<int:pk>/update/', views.department_update, name='department_update'),
    path('<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # Designation URLs
    path('designations/', views.designation_list, name='designation_list'),
    path('designations/create/', views.designation_create, name='designation_create'),
    path('designations/<int:pk>/', views.designation_detail, name='designation_detail'),
    path('designations/<int:pk>/update/', views.designation_update, name='designation_update'),
    path('designations/<int:pk>/delete/', views.designation_delete, name='designation_delete'),
] 