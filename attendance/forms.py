from django import forms
from .models import Attendance, AttendanceCorrection

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date', 'check_in', 'check_out', 'status', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class AttendanceCorrectionForm(forms.ModelForm):
    class Meta:
        model = AttendanceCorrection
        fields = ('new_check_in', 'new_check_out', 'reason')
        widgets = {
            'new_check_in': forms.TimeInput(attrs={'type': 'time'}),
            'new_check_out': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

class AttendanceCorrectionApprovalForm(forms.ModelForm):
    class Meta:
        model = AttendanceCorrection
        fields = ('status',) 