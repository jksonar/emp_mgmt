from django import forms
from django.core.validators import RegexValidator
from .models import Employee, EmployeeDocument, WorkHistory

class EmployeeForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    emergency_contact_phone = forms.CharField(validators=[phone_regex], max_length=15)
    
    class Meta:
        model = Employee
        fields = [
            'date_of_birth', 'gender', 'marital_status', 'blood_group',
            'nationality', 'religion', 'address', 'city', 'state',
            'country', 'postal_code', 'emergency_contact_name',
            'emergency_contact_relationship', 'emergency_contact_phone',
            'emergency_contact_address', 'bank_account_number', 'bank_name',
            'bank_branch', 'bank_ifsc_code', 'pan_number', 'aadhar_number',
            'passport_number', 'passport_expiry', 'joining_date',
            'probation_period', 'notice_period', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'emergency_contact_address': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['document_type', 'title', 'file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("File size should not exceed 5MB.")
        return file

class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkHistory
        fields = ['company_name', 'designation', 'start_date', 'end_date', 'is_current', 'job_description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'job_description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        is_current = cleaned_data.get('is_current')
        
        if not is_current and end_date is None:
            raise forms.ValidationError("End date is required for past employment.")
        
        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")
        
        return cleaned_data

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            'address', 'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'emergency_contact_address',
            'bank_account_number', 'bank_name', 'bank_branch',
            'pan_number', 'aadhar_number'
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'emergency_contact_address': forms.Textarea(attrs={'rows': 3}),
        } 