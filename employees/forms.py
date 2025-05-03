from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            'date_of_birth', 'gender', 'address', 
            'emergency_contact', 'emergency_contact_name',
            'bank_account_number', 'bank_name', 'bank_branch',
            'pan_number', 'aadhar_number'
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            'address', 'emergency_contact', 'emergency_contact_name',
            'bank_account_number', 'bank_name', 'bank_branch',
            'pan_number', 'aadhar_number'
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        } 