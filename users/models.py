from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr_manager', 'HR Manager'),
        ('senior_manager', 'Senior Manager'),
        ('team_manager', 'Team Manager'),
        ('team_lead', 'Team Lead'),
        ('employee', 'Employee'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey('departments.Designation', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_hr_manager(self):
        return self.role == 'hr_manager'
    
    def is_senior_manager(self):
        return self.role == 'senior_manager'
    
    def is_team_manager(self):
        return self.role == 'team_manager'
    
    def is_team_lead(self):
        return self.role == 'team_lead'
    
    def is_employee(self):
        return self.role == 'employee'
