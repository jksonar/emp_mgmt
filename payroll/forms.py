from django import forms
from django.core.validators import MinValueValidator
from employees.models import CustomUser
from .models import SalaryStructure, Payroll

class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = [
            'employee', 'basic_salary', 'hra', 'da', 'special_allowance',
            'medical_allowance', 'conveyance_allowance', 'other_allowances',
            'professional_tax', 'pf', 'esi', 'tds', 'other_deductions',
            'effective_from', 'is_active'
        ]
        widgets = {
            'effective_from': forms.DateInput(attrs={'type': 'date'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'salary_structure', 'month', 'basic_salary', 'hra', 'da',
            'special_allowance', 'medical_allowance', 'conveyance_allowance',
            'other_allowances', 'professional_tax', 'pf', 'esi', 'tds',
            'other_deductions'
        ]
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        employee = cleaned_data.get('employee')
        
        if month and employee:
            # Check if payroll record already exists for this employee and month
            existing = Payroll.objects.filter(
                employee=employee,
                month__year=month.year,
                month__month=month.month
            ).exists()
            
            if existing:
                raise forms.ValidationError(
                    "A payroll record already exists for this employee in the selected month."
                )
        
        return cleaned_data

class PayrollApprovalForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('approved', 'Approve'),
                ('rejected', 'Reject'),
            ])
        } 