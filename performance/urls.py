from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    # Performance Review URLs
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/', views.review_detail, name='review_detail'),
    path('reviews/<int:pk>/update/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/submit/', views.review_submit, name='review_submit'),
    path('reviews/<int:pk>/feedback/', views.review_feedback, name='review_feedback'),
    
    # Performance Goal URLs
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:pk>/update/', views.goal_update, name='goal_update'),
    path('goals/<int:pk>/progress/', views.goal_progress_update, name='goal_progress_update'),
] 