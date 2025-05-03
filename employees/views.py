from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Employee, EmployeeDocument, WorkHistory, CustomUser, UserProfile, Document
from .forms import EmployeeForm, EmployeeDocumentForm, WorkHistoryForm, CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, DocumentForm
from django.contrib.auth import login, logout, authenticate


@login_required
def employee_list(request):
    """List all employees"""
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, pk):
    """View employee details"""
    employee = get_object_or_404(Employee, pk=pk)
    documents = employee.documents.all()
    work_history = employee.work_history.all()
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'documents': documents,
        'work_history': work_history
    })

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee created successfully.')
        return super().form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully.')
        return super().form_valid(form)

@login_required
def employee_create(request):
    """Create a new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_update(request, pk):
    """Update employee details"""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_delete(request, pk):
    """Delete an employee"""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employees:employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

@login_required
def employee_profile(request):
    """View employee profile"""
    employee = get_object_or_404(Employee, user=request.user)
    return render(request, 'employees/employee_profile.html', {'employee': employee})

@login_required
def employee_profile_update(request):
    """Update employee profile"""
    employee = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:employee_profile')
    else:
        form = EmployeeProfileForm(instance=employee)
    return render(request, 'employees/employee_profile_form.html', {'form': form})

@login_required
def upload_document(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('employees:employee_detail', pk=employee_id)
    else:
        form = EmployeeDocumentForm()
    
    return render(request, 'employees/document_form.html', {
        'form': form,
        'employee': employee
    })

@login_required
def verify_document(request, document_id):
    if not request.user.is_hr_manager:
        messages.error(request, 'You do not have permission to verify documents.')
        return redirect('employees:employee_list')
    
    document = get_object_or_404(EmployeeDocument, pk=document_id)
    document.is_verified = True
    document.verified_by = request.user
    document.save()
    
    messages.success(request, 'Document verified successfully.')
    return redirect('employees:employee_detail', pk=document.employee.id)

@login_required
def add_work_history(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST)
        if form.is_valid():
            work_history = form.save(commit=False)
            work_history.employee = employee
            work_history.save()
            messages.success(request, 'Work history added successfully.')
            return redirect('employees:employee_detail', pk=employee_id)
    else:
        form = WorkHistoryForm()
    
    return render(request, 'employees/work_history_form.html', {
        'form': form,
        'employee': employee
    })

@login_required
def delete_work_history(request, work_history_id):
    work_history = get_object_or_404(WorkHistory, pk=work_history_id)
    employee_id = work_history.employee.id
    work_history.delete()
    messages.success(request, 'Work history deleted successfully.')
    return redirect('employees:employee_detail', pk=employee_id)

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(EmployeeDocument, pk=document_id)
    employee_id = document.employee.id
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('employees:employee_detail', pk=employee_id)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'employees/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'employees/dashboard.html')

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
