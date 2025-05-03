from django import forms
from .models import Department, Designation

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ('name', 'department', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 