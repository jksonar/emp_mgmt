from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_days = models.PositiveIntegerField(default=0)
    carry_forward = models.BooleanField(default=False)
    max_carry_forward = models.PositiveIntegerField(default=0)
    requires_approval = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Approval chain
    approved_by_team_lead = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_lead_approvals')
    approved_by_team_manager = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_manager_approvals')
    approved_by_senior_manager = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='senior_manager_approvals')
    approved_by_hr = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_approvals')
    
    # Approval timestamps
    team_lead_approved_at = models.DateTimeField(null=True, blank=True)
    team_manager_approved_at = models.DateTimeField(null=True, blank=True)
    senior_manager_approved_at = models.DateTimeField(null=True, blank=True)
    hr_approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        if not self.days:
            self.days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)

class LeaveBalance(models.Model):
    employee = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    total_days = models.PositiveIntegerField(default=0)
    used_days = models.PositiveIntegerField(default=0)
    carried_forward = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=timezone.now().year)
    
    class Meta:
        unique_together = ['employee', 'leave_type', 'year']
        ordering = ['employee', 'leave_type']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.leave_type.name} ({self.year})"
    
    @property
    def available_days(self):
        return self.total_days + self.carried_forward - self.used_days
