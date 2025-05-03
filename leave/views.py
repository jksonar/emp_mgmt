from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
import csv
from datetime import datetime
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

class LeaveTypeListView(LoginRequiredMixin, ListView):
    model = LeaveType
    template_name = 'leave/type_list.html'
    context_object_name = 'types'

class LeaveTypeCreateView(LoginRequiredMixin, CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leave/type_form.html'
    success_url = reverse_lazy('leave:type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Leave type created successfully.')
        return super().form_valid(form)

class LeaveTypeDetailView(LoginRequiredMixin, DetailView):
    model = LeaveType
    template_name = 'leave/type_detail.html'
    context_object_name = 'type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = LeaveApplication.objects.filter(
            leave_type=self.object
        ).select_related('employee').order_by('-created_at')[:10]
        return context

class LeaveTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leave/type_form.html'
    success_url = reverse_lazy('leave:type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Leave type updated successfully.')
        return super().form_valid(form)

class LeaveTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaveType
    template_name = 'leave/type_confirm_delete.html'
    success_url = reverse_lazy('leave:type_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Leave type deleted successfully.')
        return super().delete(request, *args, **kwargs)

class LeaveApplicationListView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = 'leave/application_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return LeaveApplication.objects.filter(employee=self.request.user).select_related(
            'leave_type'
        ).order_by('-created_at')

class LeaveApplicationCreateView(LoginRequiredMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'leave/application_form.html'
    success_url = reverse_lazy('leave:application_list')
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        messages.success(self.request, 'Leave application submitted successfully.')
        return super().form_valid(form)

class LeaveApplicationDetailView(LoginRequiredMixin, DetailView):
    model = LeaveApplication
    template_name = 'leave/application_detail.html'
    context_object_name = 'leave'

class LeaveApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'leave/application_form.html'
    success_url = reverse_lazy('leave:application_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Leave application updated successfully.')
        return super().form_valid(form)

class LeaveApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = LeaveApplication
    template_name = 'leave/application_confirm_delete.html'
    success_url = reverse_lazy('leave:application_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Leave application deleted successfully.')
        return super().delete(request, *args, **kwargs)

class PendingLeaveListView(LoginRequiredMixin, ListView):
    model = LeaveApplication
    template_name = 'leave/pending_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return LeaveApplication.objects.filter(status='pending').select_related(
            'employee', 'leave_type'
        ).order_by('-created_at')

class LeaveBalanceListView(LoginRequiredMixin, ListView):
    model = LeaveBalance
    template_name = 'leave/balance_list.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return LeaveBalance.objects.filter(employee=self.request.user).select_related(
            'leave_type'
        ).order_by('leave_type')

class LeaveBalanceDetailView(LoginRequiredMixin, DetailView):
    model = LeaveBalance
    template_name = 'leave/balance_detail.html'
    context_object_name = 'balance'

class LeaveBalanceUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveBalance
    form_class = LeaveBalanceForm
    template_name = 'leave/balance_form.html'
    success_url = reverse_lazy('leave:balance_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Leave balance updated successfully.')
        return super().form_valid(form)

class LeaveSummaryReportView(LoginRequiredMixin, TemplateView):
    template_name = 'leave/summary_report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current year
        current_year = timezone.now().year
        
        # Leave applications by status
        context['leave_status'] = LeaveApplication.objects.filter(
            created_at__year=current_year
        ).values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Leave applications by type
        context['leave_types'] = LeaveApplication.objects.filter(
            created_at__year=current_year
        ).values('leave_type__name').annotate(
            count=Count('id'),
            total_days=Sum('days')
        ).order_by('leave_type__name')
        
        # Monthly leave trends
        monthly_data = LeaveApplication.objects.filter(
            created_at__year=current_year
        ).extra(
            select={'month': "EXTRACT(month FROM created_at)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        context['monthly_data'] = monthly_data
        
        # Department-wise leave distribution
        context['department_data'] = LeaveApplication.objects.filter(
            created_at__year=current_year
        ).values('employee__department__name').annotate(
            count=Count('id'),
            total_days=Sum('days')
        ).order_by('employee__department__name')
        
        return context

def export_leave_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="leave_report_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Employee ID',
        'Employee Name',
        'Department',
        'Leave Type',
        'Start Date',
        'End Date',
        'Days',
        'Status',
        'Applied On',
        'Approved By',
        'Approved On'
    ])
    
    leaves = LeaveApplication.objects.select_related(
        'employee',
        'employee__department',
        'leave_type',
        'approved_by'
    ).order_by('-created_at')
    
    for leave in leaves:
        writer.writerow([
            leave.employee.employee_id,
            leave.employee.get_full_name(),
            leave.employee.department.name,
            leave.leave_type.name,
            leave.start_date,
            leave.end_date,
            leave.days,
            leave.get_status_display(),
            leave.created_at,
            leave.approved_by.get_full_name() if leave.approved_by else '',
            leave.approved_at if leave.approved_at else ''
        ])
    
    return response

@login_required
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave application approved successfully.')
    else:
        messages.error(request, 'You do not have permission to approve leaves.')
    return redirect('leave:application_detail', pk=pk)

@login_required
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if request.user.is_superuser or request.user.is_staff:
        leave.status = 'rejected'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave application rejected successfully.')
    else:
        messages.error(request, 'You do not have permission to reject leaves.')
    return redirect('leave:application_detail', pk=pk)

@login_required
def cancel_leave(request, pk):
    leave = get_object_or_404(LeaveApplication, pk=pk)
    if leave.employee == request.user and leave.status == 'pending':
        leave.status = 'cancelled'
        leave.save()
        messages.success(request, 'Leave application cancelled successfully.')
    else:
        messages.error(request, 'You cannot cancel this leave application.')
    return redirect('leave:application_detail', pk=pk)
