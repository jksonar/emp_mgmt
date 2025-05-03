from django.db import models
from django.conf import settings

class PerformanceReview(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('self_review', 'Self Review'),
        ('team_lead_review', 'Team Lead Review'),
        ('manager_review', 'Manager Review'),
        ('senior_manager_review', 'Senior Manager Review'),
        ('hr_review', 'HR Review'),
        ('completed', 'Completed'),
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_reviews')
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    self_assessment = models.TextField(blank=True)
    team_lead_feedback = models.TextField(blank=True)
    manager_feedback = models.TextField(blank=True)
    senior_manager_feedback = models.TextField(blank=True)
    hr_feedback = models.TextField(blank=True)
    self_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    team_lead_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    manager_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    senior_manager_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    final_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_period_end']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.review_period_start} to {self.review_period_end}"
    
    def calculate_final_rating(self):
        ratings = [
            self.team_lead_rating,
            self.manager_rating,
            self.senior_manager_rating
        ]
        valid_ratings = [r for r in ratings if r is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return None

class PerformanceGoal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_goals')
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
