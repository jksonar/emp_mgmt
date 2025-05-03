from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'department', 'designation', 'date_of_joining')
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'department', 'designation', 'date_of_joining', 'profile_picture')
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'gender', 'address', 'emergency_contact_name', 
                 'emergency_contact_relationship', 'emergency_contact_phone', 
                 'emergency_contact_address', 'blood_group', 'nationality', 
                 'marital_status', 'religion', 'avatar')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'emergency_contact_address': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture') 