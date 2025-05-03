from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import LeaveType, LeaveApplication, LeaveBalance
from .forms import LeaveTypeForm, LeaveApplicationForm, LeaveBalanceForm

@login_required
def leave_type_list(request):
    """List all leave types"""
    leave_types = LeaveType.objects.all()
    return render(request, 'leave/leave_type_list.html', {'leave_types': leave_types})

@login_required
def leave_type_create(request):
    """Create a new leave type"""
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave:leave_type_list')
    else:
        form = LeaveTypeForm()
    return render(request, 'leave/leave_type_form.html', {'form': form})

@login_required
def leave_type_detail(request, pk):
    """View leave type details"""
    leave_type = get_object_or_404(LeaveType, pk=pk)
    return render(request, 'leave/leave_type_detail.html', {'leave_type': leave_type})

@login_required
def leave_type_update(request, pk):
    """Update leave type details"""
    leave_type = get_object_or_404(LeaveType, pk=pk)
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST, instance=leave_type)
        if form.is_valid():
            form.save()
            return redirect('leave:leave_type_detail', pk=leave_type.pk)
    else:
        form = LeaveTypeForm(instance=leave_type)
    return render(request, 'leave/leave_type_form.html', {'form': form})

@login_required
def leave_type_delete(request, pk):
    """Delete a leave type"""
    leave_type = get_object_or_404(LeaveType, pk=pk)
    if request.method == 'POST':
        leave_type.delete()
        return redirect('leave:leave_type_list')
    return render(request, 'leave/leave_type_confirm_delete.html', {'leave_type': leave_type})

@login_required
def leave_list(request):
    """List all leave applications"""
    leaves = LeaveApplication.objects.all()
    return render(request, 'leave/leave_list.html', {'leaves': leaves})

@login_required
def leave_apply(request):
    """Apply for leave"""
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            return redirect('leave:leave_detail', pk=leave.pk)
    else:
        form = LeaveApplicationForm()
    return render(request, 'leave/leave_form.html', {'form': form})

@login_required
def leave_detail(request, pk):
    """View leave application details"""
    leave = get_object_or_404(LeaveApplication, pk=pk)
    return render(request, 'leave/leave_detail.html', {'leave': leave})

@login_required
def leave_update(request, pk):
    """Update leave application"""
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave:leave_detail', pk=leave.pk)
    else:
        form = LeaveApplicationForm(instance=leave)
    return render(request, 'leave/leave_form.html', {'form': form})

@login_required
def leave_cancel(request, pk):
    """Cancel a leave application"""
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        leave.status = 'cancelled'
        leave.save()
        return redirect('leave:leave_detail', pk=leave.pk)
    return render(request, 'leave/leave_cancel.html', {'leave': leave})

@login_required
def leave_approve(request, pk):
    """Approve a leave application"""
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.approved_at = timezone.now()
        leave.save()
        return redirect('leave:leave_detail', pk=leave.pk)
    return render(request, 'leave/leave_approve.html', {'leave': leave})

@login_required
def leave_balance_list(request):
    """List all leave balances"""
    balances = LeaveBalance.objects.all()
    return render(request, 'leave/leave_balance_list.html', {'balances': balances})

@login_required
def leave_balance_detail(request, pk):
    """View leave balance details"""
    balance = get_object_or_404(LeaveBalance, pk=pk)
    return render(request, 'leave/leave_balance_detail.html', {'balance': balance})
