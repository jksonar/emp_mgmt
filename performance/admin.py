from django.contrib import admin
from .models import (
    PerformanceCycle,
    KPI,
    PerformanceReview,
    KPIReview,
    DevelopmentPlan,
    PerformanceGoal
)

@admin.register(PerformanceCycle)
class PerformanceCycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'description')

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'weight', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'cycle', 'status', 'final_rating')
    list_filter = ('status', 'cycle')
    search_fields = ('employee__first_name', 'employee__last_name', 'cycle__name')

@admin.register(KPIReview)
class KPIReviewAdmin(admin.ModelAdmin):
    list_display = ('performance_review', 'kpi', 'self_rating', 'manager_rating')
    list_filter = ('kpi',)
    search_fields = ('performance_review__employee__first_name', 'performance_review__employee__last_name')

@admin.register(DevelopmentPlan)
class DevelopmentPlanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'status', 'progress')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'title')

@admin.register(PerformanceGoal)
class PerformanceGoalAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'status', 'progress')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'title')
