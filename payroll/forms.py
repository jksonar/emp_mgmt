from django import forms
from .models import SalaryStructure, PayrollRecord

class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = ('name', 'description', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = PayrollRecord
        fields = (
            'employee', 'salary_structure', 'month', 'basic_salary',
            'status'
        )
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        employee = cleaned_data.get('employee')
        
        if month and employee:
            # Check if payroll record already exists for this employee and month
            existing = PayrollRecord.objects.filter(
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
        model = PayrollRecord
        fields = ('status',) 