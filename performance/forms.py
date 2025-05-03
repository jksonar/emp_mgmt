from django import forms
from .models import PerformanceReview, PerformanceGoal, PerformanceCycle, KPIReview

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = (
            'cycle', 'self_rating', 'strengths', 'areas_for_improvement',
            'goals_for_next_cycle', 'comments'
        )
        widgets = {
            'self_rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
            'strengths': forms.Textarea(attrs={'rows': 3}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 3}),
            'goals_for_next_cycle': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class PerformanceFeedbackForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ('manager_rating', 'comments')
        widgets = {
            'manager_rating': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
            'comments': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.status == 'manager_review':
                self.fields['manager_rating'].label = 'Manager Rating'
                self.fields['comments'].label = 'Manager Comments'
            elif instance.status == 'hr_review':
                self.fields['manager_rating'].label = 'HR Rating'
                self.fields['comments'].label = 'HR Comments'

class KPIReviewForm(forms.ModelForm):
    class Meta:
        model = KPIReview
        fields = ('self_rating', 'self_comments')
        widgets = {
            'self_rating': forms.Select(choices=KPIReview.RATING_CHOICES),
            'self_comments': forms.Textarea(attrs={'rows': 3}),
        }

class ManagerKPIReviewForm(forms.ModelForm):
    class Meta:
        model = KPIReview
        fields = ('manager_rating', 'manager_comments')
        widgets = {
            'manager_rating': forms.Select(choices=KPIReview.RATING_CHOICES),
            'manager_comments': forms.Textarea(attrs={'rows': 3}),
        }

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