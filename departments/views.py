from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Department, Designation
from .forms import DepartmentForm, DesignationForm

@login_required
def department_list(request):
    """List all departments"""
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    """Create a new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})

@login_required
def department_detail(request, pk):
    """View department details"""
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'departments/department_detail.html', {'department': department})

@login_required
def department_update(request, pk):
    """Update department details"""
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('departments:department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form})

@login_required
def department_delete(request, pk):
    """Delete a department"""
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('departments:department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})

@login_required
def designation_list(request):
    """List all designations"""
    designations = Designation.objects.all()
    return render(request, 'departments/designation_list.html', {'designations': designations})

@login_required
def designation_create(request):
    """Create a new designation"""
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments:designation_list')
    else:
        form = DesignationForm()
    return render(request, 'departments/designation_form.html', {'form': form})

@login_required
def designation_detail(request, pk):
    """View designation details"""
    designation = get_object_or_404(Designation, pk=pk)
    return render(request, 'departments/designation_detail.html', {'designation': designation})

@login_required
def designation_update(request, pk):
    """Update designation details"""
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation)
        if form.is_valid():
            form.save()
            return redirect('departments:designation_detail', pk=designation.pk)
    else:
        form = DesignationForm(instance=designation)
    return render(request, 'departments/designation_form.html', {'form': form})

@login_required
def designation_delete(request, pk):
    """Delete a designation"""
    designation = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        designation.delete()
        return redirect('departments:designation_list')
    return render(request, 'departments/designation_confirm_delete.html', {'designation': designation})
