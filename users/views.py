from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import pyotp
from django.utils import timezone
from .models import UserProfile, Document, CustomUser
from .forms import UserProfileForm, ProfileUpdateForm, DocumentForm

# Create your views here.

@login_required
def profile(request):
    """View user profile"""
    profile = UserProfile.objects.get(user=request.user)
    documents = Document.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {
        'profile': profile,
        'documents': documents
    })

@login_required
def profile_update(request):
    """Update user profile"""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard with overview of all modules"""
    context = {
        'user': request.user,
        'profile': UserProfile.objects.get(user=request.user),
        'documents': Document.objects.filter(user=request.user),
        'leave_balance': request.user.leave_balances.all(),
        'recent_attendance': request.user.attendance_records.order_by('-date')[:5],
        'pending_leave': request.user.leave_applications.filter(status='pending'),
        'performance_reviews': request.user.performance_reviews.order_by('-cycle__start_date')[:3],
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def upload_document(request):
    """Upload a new document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('users:profile')
    else:
        form = DocumentForm()
    return render(request, 'users/upload_document.html', {'form': form})

@login_required
def verify_document(request, document_id):
    """Verify a document (HR only)"""
    if not request.user.is_hr_manager():
        messages.error(request, 'You do not have permission to verify documents.')
        return redirect('users:profile')
    
    document = get_object_or_404(Document, id=document_id)
    document.is_verified = True
    document.verified_by = request.user
    document.verified_at = timezone.now()
    document.save()
    
    messages.success(request, 'Document verified successfully.')
    return redirect('users:profile')

@login_required
def setup_2fa(request):
    """Setup two-factor authentication"""
    if request.method == 'POST':
        secret = pyotp.random_base32()
        request.user.two_factor_secret = secret
        request.user.save()
        
        # Generate QR code URL
        totp = pyotp.TOTP(secret)
        qr_code_url = totp.provisioning_uri(request.user.email, issuer_name="Employee Management System")
        
        return render(request, 'users/setup_2fa.html', {
            'qr_code_url': qr_code_url,
            'secret': secret
        })
    
    return render(request, 'users/setup_2fa.html')

@login_required
def verify_2fa(request):
    """Verify two-factor authentication setup"""
    if request.method == 'POST':
        token = request.POST.get('token')
        secret = request.user.two_factor_secret
        
        if pyotp.TOTP(secret).verify(token):
            request.user.two_factor_enabled = True
            request.user.save()
            messages.success(request, 'Two-factor authentication enabled successfully.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Invalid token. Please try again.')
    
    return render(request, 'users/verify_2fa.html')

@login_required
def disable_2fa(request):
    """Disable two-factor authentication"""
    if request.method == 'POST':
        request.user.two_factor_enabled = False
        request.user.two_factor_secret = ''
        request.user.save()
        messages.success(request, 'Two-factor authentication disabled successfully.')
        return redirect('users:profile')
    
    return render(request, 'users/disable_2fa.html')

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'users/document_list.html'
    context_object_name = 'documents'
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
