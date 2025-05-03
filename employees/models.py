from django.db import models
from django.conf import settings
from departments.models import Department, Designation
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser

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
        return f"{self.user.get_full_name()}'s {self.get_document_type_display()}"

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_address = models.TextField(blank=True)
    
    # Bank Details
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)
    bank_ifsc_code = models.CharField(max_length=11, blank=True)
    
    # Government IDs
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    
    # Additional Information
    joining_date = models.DateField(null=True, blank=True)
    probation_period = models.IntegerField(default=3)  # in months
    notice_period = models.IntegerField(default=30)  # in days
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            # Generate employee ID based on department and joining date
            department_code = self.user.department.name[:3].upper() if self.user.department else 'EMP'
            year = self.user.date_of_joining.year if self.user.date_of_joining else '0000'
            last_employee = Employee.objects.filter(employee_id__startswith=f"{department_code}{year}").order_by('-employee_id').first()
            
            if last_employee:
                last_number = int(last_employee.employee_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.employee_id = f"{department_code}{year}{str(new_number).zfill(4)}"
        
        super().save(*args, **kwargs)

class EmployeeDocument(models.Model):
    DOCUMENT_TYPES = [
        ('resume', 'Resume'),
        ('offer_letter', 'Offer Letter'),
        ('joining_letter', 'Joining Letter'),
        ('experience_letter', 'Experience Letter'),
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('educational_certificate', 'Educational Certificate'),
        ('other', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_employee_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.get_document_type_display()}"

class WorkHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_history')
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    job_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = 'Work Histories'
    
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.company_name}"
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Update other work histories to not be current
            WorkHistory.objects.filter(employee=self.employee, is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)
