from django.db import models
from django.conf import settings
from departments.models import Department, Designation

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
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
