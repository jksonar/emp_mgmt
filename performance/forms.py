from django import forms
from .models import PerformanceReview, PerformanceGoal

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = (
            'review_period_start', 'review_period_end',
            'self_assessment', 'self_rating'
        )
        widgets = {
            'review_period_start': forms.DateInput(attrs={'type': 'date'}),
            'review_period_end': forms.DateInput(attrs={'type': 'date'}),
            'self_assessment': forms.Textarea(attrs={'rows': 5}),
            'self_rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
        }

class PerformanceFeedbackForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ('feedback', 'rating')
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.status == 'team_lead_review':
                self.fields['feedback'].label = 'Team Lead Feedback'
                self.fields['rating'].label = 'Team Lead Rating'
            elif instance.status == 'manager_review':
                self.fields['feedback'].label = 'Manager Feedback'
                self.fields['rating'].label = 'Manager Rating'
            elif instance.status == 'senior_manager_review':
                self.fields['feedback'].label = 'Senior Manager Feedback'
                self.fields['rating'].label = 'Senior Manager Rating'
            elif instance.status == 'hr_review':
                self.fields['feedback'].label = 'HR Feedback'

class PerformanceGoalForm(forms.ModelForm):
    class Meta:
        model = PerformanceGoal
        fields = ('title', 'description', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date")

class PerformanceGoalUpdateForm(forms.ModelForm):
    class Meta:
        model = PerformanceGoal
        fields = ('status', 'progress')
        widgets = {
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        } 