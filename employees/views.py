from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Employee, EmployeeDocument, WorkHistory
from .forms import EmployeeForm, EmployeeDocumentForm, WorkHistoryForm


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
