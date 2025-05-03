from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.

@login_required
def profile(request):
    """View user profile"""
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def profile_update(request):
    """Update user profile"""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard with overview of all modules"""
    context = {
        'user': request.user,
        'profile': UserProfile.objects.get(user=request.user)
    }
    return render(request, 'users/dashboard.html', context)
