from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class SalaryComponent(models.Model):
    COMPONENT_TYPES = [
        ('earning', 'Earning'),
        ('deduction', 'Deduction'),
    ]
    
    CALCULATION_TYPES = [
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage of Basic'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    is_taxable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_component_type_display()})"

class SalaryStructure(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    components = models.ManyToManyField(SalaryComponent, through='SalaryStructureComponent')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SalaryStructureComponent(models.Model):
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        unique_together = ['salary_structure', 'component']
    
    def __str__(self):
        return f"{self.salary_structure.name} - {self.component.name}"

class PayrollRecord(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='payroll_records')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-month', 'employee']
        unique_together = ['employee', 'month']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.month.strftime('%B %Y')}"
    
    def calculate_salary(self):
        # Calculate gross salary and deductions based on salary structure
        self.gross_salary = self.basic_salary
        self.total_deductions = Decimal('0.00')
        
        for structure_component in self.salary_structure.salarystructurecomponent_set.all():
            component = structure_component.component
            if component.calculation_type == 'fixed':
                amount = component.value
            else:  # percentage
                amount = (self.basic_salary * component.value) / Decimal('100.00')
            
            if component.component_type == 'earning':
                self.gross_salary += amount
            else:  # deduction
                self.total_deductions += amount
        
        self.net_salary = self.gross_salary - self.total_deductions

class Payslip(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, related_name='payslips')
    file = models.FileField(upload_to='payslips/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Payslip for {self.payroll_record}"
