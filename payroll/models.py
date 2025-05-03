from django.db import models
from django.conf import settings

class SalaryStructure(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salary_structures')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_from = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_from']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.effective_from}"
    
    @property
    def gross_salary(self):
        return sum([
            self.basic_salary,
            self.hra,
            self.da,
            self.special_allowance,
            self.medical_allowance,
            self.conveyance_allowance,
            self.other_allowances
        ])

class Payroll(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payrolls')
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='payrolls')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], default='draft')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['employee', 'month', 'year']
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.month}/{self.year}"
    
    def save(self, *args, **kwargs):
        if not self.net_salary:
            self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)
    
    def calculate_net_salary(self):
        gross_salary = sum([
            self.basic_salary,
            self.hra,
            self.da,
            self.special_allowance,
            self.medical_allowance,
            self.conveyance_allowance,
            self.other_allowances
        ])
        
        total_deductions = sum([
            self.professional_tax,
            self.income_tax,
            self.provident_fund,
            self.other_deductions
        ])
        
        return gross_salary - total_deductions
