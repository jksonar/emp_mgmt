from django.db import models
from django.conf import settings

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-check_in']
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date} ({self.status})"
    
    def calculate_working_hours(self):
        if self.check_in and self.check_out:
            from datetime import datetime, timedelta
            check_in = datetime.combine(self.date, self.check_in)
            check_out = datetime.combine(self.date, self.check_out)
            if check_out < check_in:
                check_out += timedelta(days=1)
            return (check_out - check_in).total_seconds() / 3600
        return 0

class AttendanceCorrection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='corrections')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_corrections')
    new_check_in = models.TimeField(null=True, blank=True)
    new_check_out = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_corrections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Correction for {self.attendance} - {self.status}"
