from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import SalaryStructure, Payroll, Payslip
from .forms import SalaryStructureForm, PayrollForm, PayrollApprovalForm

@login_required
def salary_structure_list(request):
    """List all salary structures"""
    structures = SalaryStructure.objects.all()
    return render(request, 'payroll/salary_structure_list.html', {'structures': structures})

@login_required
def salary_structure_create(request):
    """Create a new salary structure"""
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll:salary_structure_list')
    else:
        form = SalaryStructureForm()
    return render(request, 'payroll/salary_structure_form.html', {'form': form})

@login_required
def salary_structure_detail(request, pk):
    """View salary structure details"""
    structure = get_object_or_404(SalaryStructure, pk=pk)
    return render(request, 'payroll/salary_structure_detail.html', {'structure': structure})

@login_required
def salary_structure_update(request, pk):
    """Update salary structure details"""
    structure = get_object_or_404(SalaryStructure, pk=pk)
    if request.method == 'POST':
        form = SalaryStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            return redirect('payroll:salary_structure_detail', pk=structure.pk)
    else:
        form = SalaryStructureForm(instance=structure)
    return render(request, 'payroll/salary_structure_form.html', {'form': form})

@login_required
def payroll_list(request):
    """List all payroll records"""
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})

@login_required
def payroll_create(request):
    """Create a new payroll record"""
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save()
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollForm()
    return render(request, 'payroll/payroll_form.html', {'form': form})

@login_required
def payroll_detail(request, pk):
    """View payroll details"""
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})

@login_required
def payroll_update(request, pk):
    """Update payroll details"""
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollForm(instance=payroll)
    return render(request, 'payroll/payroll_form.html', {'form': form})

@login_required
def payroll_approve(request, pk):
    """Approve a payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollApprovalForm(request.POST, instance=payroll)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.status = 'approved'
            payroll.approved_by = request.user
            payroll.approved_at = timezone.now()
            payroll.save()
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollApprovalForm(instance=payroll)
    return render(request, 'payroll/payroll_approve.html', {'form': form, 'payroll': payroll})

@login_required
def payslip_generate(request, pk):
    """Generate payslip for a payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    payslip = Payslip.objects.create(
        payroll=payroll,
        employee=payroll.employee,
        basic_salary=payroll.basic_salary,
        hra=payroll.hra,
        da=payroll.da,
        ta=payroll.ta,
        pf=payroll.pf,
        tax=payroll.tax,
        other_deductions=payroll.other_deductions,
        net_salary=payroll.net_salary
    )
    return render(request, 'payroll/payslip_detail.html', {'payslip': payslip})

@login_required
def monthly_payroll_report(request):
    """Generate monthly payroll report"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    payrolls = Payroll.objects.filter(
        month=month,
        year=year
    )
    return render(request, 'payroll/monthly_report.html', {
        'month': month,
        'year': year,
        'payrolls': payrolls
    })

@login_required
def employee_payroll_report(request):
    """Generate employee-specific payroll report"""
    employee_id = request.GET.get('employee_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    payrolls = Payroll.objects.all()
    if employee_id:
        payrolls = payrolls.filter(employee_id=employee_id)
    if start_date:
        payrolls = payrolls.filter(date__gte=start_date)
    if end_date:
        payrolls = payrolls.filter(date__lte=end_date)
        
    return render(request, 'payroll/employee_report.html', {
        'payrolls': payrolls,
        'employee_id': employee_id,
        'start_date': start_date,
        'end_date': end_date
    })
