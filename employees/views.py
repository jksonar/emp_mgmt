from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser, UserProfile, Document, WorkHistory
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, DocumentForm, WorkHistoryForm
from django.contrib.auth import login, logout, authenticate
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
from departments.models import Department
from attendance.models import Attendance
from leave.models import LeaveApplication

class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'employees/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.all().select_related('department', 'designation')

class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'employees/user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = self.object.documents.all()
        context['work_history'] = self.object.work_history.all()
        return context

class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'employees/user_form.html'
    success_url = reverse_lazy('employees:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'User created successfully.')
        return super().form_valid(form)

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'employees/user_form.html'
    success_url = reverse_lazy('employees:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

class CustomUserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'employees/user_confirm_delete.html'
    success_url = reverse_lazy('employees:user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'employees/profile.html', {'profile': profile})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('employees:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'employees/profile_form.html', {'form': form})

@login_required
def document_list(request):
    documents = request.user.documents.all()
    return render(request, 'employees/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('employees:document_list')
    else:
        form = DocumentForm()
    
    return render(request, 'employees/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('employees:document_list')

@login_required
def work_history_list(request):
    work_history = request.user.work_history.all()
    return render(request, 'employees/work_history_list.html', {'work_history': work_history})

@login_required
def work_history_create(request):
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST)
        if form.is_valid():
            work_history = form.save(commit=False)
            work_history.user = request.user
            work_history.save()
            messages.success(request, 'Work history added successfully.')
            return redirect('employees:work_history_list')
    else:
        form = WorkHistoryForm()
    
    return render(request, 'employees/work_history_form.html', {'form': form})

@login_required
def work_history_update(request, pk):
    work_history = get_object_or_404(WorkHistory, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST, instance=work_history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work history updated successfully.')
            return redirect('employees:work_history_list')
    else:
        form = WorkHistoryForm(instance=work_history)
    
    return render(request, 'employees/work_history_form.html', {'form': form})

@login_required
def work_history_delete(request, pk):
    work_history = get_object_or_404(WorkHistory, pk=pk, user=request.user)
    work_history.delete()
    messages.success(request, 'Work history deleted successfully.')
    return redirect('employees:work_history_list')

@login_required
def dashboard(request):
    return render(request, 'employees/dashboard.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('employees:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'employees/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# @login_required
# def profile(request):
#     """View user profile"""
#     profile = UserProfile.objects.get(user=request.user)
#     documents = Document.objects.filter(user=request.user)
#     return render(request, 'employees/profile.html', {
#         'profile': profile,
#         'documents': documents
#     })

@login_required
def profile_update(request):
    """Update user profile"""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('employees:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'employees/profile_update.html', {'form': form})

# @login_required
# def dashboard(request):
#     """User dashboard with overview of all modules"""
#     # Get or create user profile
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if created:
#         messages.info(request, 'Welcome! Your profile has been created.')
    
#     # Get employee instance if it exists
#     try:
#         employee = request.user.employee
#         recent_attendance = employee.attendance_records.order_by('-date')[:5]
#         pending_leave = employee.leave_applications.filter(status='pending')
#         leave_balance = employee.leave_balances.all()
#         performance_reviews = employee.performance_reviews.order_by('-cycle__start_date')[:3]
#     except Employee.DoesNotExist:
#         # If user is not an employee, set empty querysets
#         employee = None
#         recent_attendance = []
#         pending_leave = []
#         leave_balance = []
#         performance_reviews = []
    
#     context = {
#         'user': request.user,
#         'profile': profile,
#         'employee': employee,
#         'documents': Document.objects.filter(user=request.user),
#         'leave_balance': leave_balance,
#         'recent_attendance': recent_attendance,
#         'pending_leave': pending_leave,
#         'performance_reviews': performance_reviews,
#     }
#     return render(request, 'employees/dashboard.html', context)

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
            return redirect('employees:profile')
    else:
        form = DocumentForm()
    return render(request, 'employees/upload_document.html', {'form': form})

@login_required
def verify_document(request, document_id):
    """Verify a document (HR only)"""
    if not request.user.is_hr_manager():
        messages.error(request, 'You do not have permission to verify documents.')
        return redirect('employees:profile')
    
    document = get_object_or_404(Document, id=document_id)
    document.is_verified = True
    document.verified_by = request.user
    document.verified_at = timezone.now()
    document.save()
    
    messages.success(request, 'Document verified successfully.')
    return redirect('employees:profile')

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
        
        return render(request, 'employees/setup_2fa.html', {
            'qr_code_url': qr_code_url,
            'secret': secret
        })
    
    return render(request, 'employees/setup_2fa.html')

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
            return redirect('employees:profile')
        else:
            messages.error(request, 'Invalid token. Please try again.')
    
    return render(request, 'employees/verify_2fa.html')

@login_required
def disable_2fa(request):
    """Disable two-factor authentication"""
    if request.method == 'POST':
        request.user.two_factor_enabled = False
        request.user.two_factor_secret = ''
        request.user.save()
        messages.success(request, 'Two-factor authentication disabled successfully.')
        return redirect('employees:profile')
    
    return render(request, 'employees/disable_2fa.html')

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'employees/document_list.html'
    context_object_name = 'documents'
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

@login_required
def home(request):
    context = {}
    
    if request.user.is_authenticated:
        # Get total employees
        context['total_employees'] = Employee.objects.count()
        
        # Get present employees today
        today = timezone.now().date()
        context['present_today'] = Attendance.objects.filter(
            date=today,
            status='present'
        ).count()
        
        # Get pending leaves
        context['pending_leaves'] = LeaveApplication.objects.filter(
            status='pending'
        ).count()
        
        # Get total departments
        context['total_departments'] = Department.objects.count()
        
        # Get recent attendance
        context['recent_attendance'] = Attendance.objects.select_related(
            'employee'
        ).order_by('-date', '-check_in')[:5]
        
        # Get recent leaves
        context['recent_leaves'] = LeaveApplication.objects.select_related(
            'employee',
            'leave_type'
        ).order_by('-created_at')[:5]
    
    return render(request, 'employees/home.html', context)
