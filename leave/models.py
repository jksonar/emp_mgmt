from django.db import models
from django.conf import settings

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_days = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Leave(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.start_date} to {self.end_date})"
    
    def calculate_days(self):
        from datetime import timedelta
        return (self.end_date - self.start_date).days + 1

class LeaveBalance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='balances')
    year = models.PositiveIntegerField()
    total_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'leave_type']
        unique_together = ['employee', 'leave_type', 'year']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.year})"
    
    @property
    def remaining_days(self):
        return self.total_days - self.used_days
