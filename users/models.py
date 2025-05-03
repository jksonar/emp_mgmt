from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, blank=True)
    
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
    
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey('departments.Designation', on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    salary_structure = models.ForeignKey('payroll.SalaryStructure', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate employee ID: YYMMDD + 4 random digits
            date_str = timezone.now().strftime('%y%m%d')
            random_str = str(uuid.uuid4().int)[:4]
            self.employee_id = f"{date_str}{random_str}"
        super().save(*args, **kwargs)
    
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

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    documents = models.ManyToManyField('Document', blank=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('offer_letter', 'Offer Letter'),
        ('joining_letter', 'Joining Letter'),
        ('resume', 'Resume'),
        ('certificate', 'Certificate'),
        ('id_proof', 'ID Proof'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_user_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_document_type_display()}"
