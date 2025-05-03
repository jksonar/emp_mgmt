from django import forms
from .models import SalaryStructure, Payroll

class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = (
            'basic_salary', 'hra', 'da', 'special_allowance',
            'medical_allowance', 'conveyance_allowance', 'other_allowances',
            'effective_from'
        )
        widgets = {
            'effective_from': forms.DateInput(attrs={'type': 'date'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = (
            'month', 'year', 'basic_salary', 'hra', 'da',
            'special_allowance', 'medical_allowance', 'conveyance_allowance',
            'other_allowances', 'professional_tax', 'income_tax',
            'provident_fund', 'other_deductions'
        )
        widgets = {
            'month': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2100}),
        }

class PayrollApprovalForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ('status', 'payment_date')
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        } 