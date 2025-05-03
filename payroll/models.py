from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MinValueValidator
from employees.models import CustomUser

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
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='salary_structures')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    da = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    pf = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    esi = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tds = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    effective_from = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.effective_from}"

    class Meta:
        ordering = ['-effective_from']

class SalaryStructureComponent(models.Model):
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        unique_together = ['salary_structure', 'component']
    
    def __str__(self):
        return f"{self.salary_structure.employee.username} - {self.component.name}"

class Payroll(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payrolls')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    month = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    da = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    pf = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    esi = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tds = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payrolls')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%B %Y')}"

    class Meta:
        ordering = ['-month']
        unique_together = ['employee', 'month']

class Payslip(models.Model):
    payroll_record = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='payslips')
    file = models.FileField(upload_to='payslips/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Payslip for {self.payroll_record}"
