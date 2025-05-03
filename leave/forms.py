from django import forms
from .models import LeaveApplication, LeaveType, LeaveBalance

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ('name', 'description', 'max_days', 'carry_forward', 'max_carry_forward', 'requires_approval', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ('leave_type', 'start_date', 'end_date', 'reason')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date")

class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ('status',)

class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = ('leave_type', 'year', 'total_days') 