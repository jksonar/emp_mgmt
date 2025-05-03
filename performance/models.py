from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class PerformanceCycle(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        unique_together = ['name', 'start_date']
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

class KPI(models.Model):
    CATEGORY_CHOICES = [
        ('quantitative', 'Quantitative'),
        ('qualitative', 'Qualitative'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
    
    def __str__(self):
        return self.name

class PerformanceReview(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('self_review', 'Self Review'),
        ('manager_review', 'Manager Review'),
        ('hr_review', 'HR Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey('employees.CustomUser', on_delete=models.CASCADE, related_name='performance_reviews')
    cycle = models.ForeignKey(PerformanceCycle, on_delete=models.CASCADE, related_name='reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    self_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    manager_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    goals_for_next_cycle = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-cycle__start_date', 'employee']
        unique_together = ['employee', 'cycle']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.cycle.name}"

class KPIReview(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='kpi_reviews')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    self_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    manager_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    self_comments = models.TextField(blank=True)
    manager_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['kpi__name']
        unique_together = ['performance_review', 'kpi']
    
    def __str__(self):
        return f"{self.performance_review} - {self.kpi.name}"

class DevelopmentPlan(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey('employees.CustomUser', on_delete=models.CASCADE, related_name='development_plans')
    performance_review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE, related_name='development_plans')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    progress = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.title}"

class PerformanceGoal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey('employees.CustomUser', on_delete=models.CASCADE, related_name='performance_goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.title}"
