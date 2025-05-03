from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import SalaryStructure, Payroll, Payslip
from .forms import SalaryStructureForm, PayrollForm, PayrollApprovalForm
from employees.models import CustomUser

class SalaryStructureListView(LoginRequiredMixin, ListView):
    model = SalaryStructure
    template_name = 'payroll/salary_structure_list.html'
    context_object_name = 'structures'

class SalaryStructureDetailView(LoginRequiredMixin, DetailView):
    model = SalaryStructure
    template_name = 'payroll/salary_structure_detail.html'
    context_object_name = 'structure'

class SalaryStructureCreateView(LoginRequiredMixin, CreateView):
    model = SalaryStructure
    form_class = SalaryStructureForm
    template_name = 'payroll/salary_structure_form.html'
    success_url = reverse_lazy('payroll:salary_structure_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Salary structure created successfully.')
        return super().form_valid(form)

class SalaryStructureUpdateView(LoginRequiredMixin, UpdateView):
    model = SalaryStructure
    form_class = SalaryStructureForm
    template_name = 'payroll/salary_structure_form.html'
    success_url = reverse_lazy('payroll:salary_structure_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Salary structure updated successfully.')
        return super().form_valid(form)

class SalaryStructureDeleteView(LoginRequiredMixin, DeleteView):
    model = SalaryStructure
    template_name = 'payroll/salary_structure_confirm_delete.html'
    success_url = reverse_lazy('payroll:salary_structure_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Salary structure deleted successfully.')
        return super().delete(request, *args, **kwargs)

class PayrollListView(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = 'payroll/payroll_list.html'
    context_object_name = 'payrolls'

class PayrollDetailView(LoginRequiredMixin, DetailView):
    model = Payroll
    template_name = 'payroll/payroll_detail.html'
    context_object_name = 'payroll'

class PayrollCreateView(LoginRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll/payroll_form.html'
    success_url = reverse_lazy('payroll:payroll_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Payroll created successfully.')
        return super().form_valid(form)

class PayrollUpdateView(LoginRequiredMixin, UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll/payroll_form.html'
    success_url = reverse_lazy('payroll:payroll_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Payroll updated successfully.')
        return super().form_valid(form)

class PayrollDeleteView(LoginRequiredMixin, DeleteView):
    model = Payroll
    template_name = 'payroll/payroll_confirm_delete.html'
    success_url = reverse_lazy('payroll:payroll_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Payroll deleted successfully.')
        return super().delete(request, *args, **kwargs)

@login_required
def approve_payroll(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollApprovalForm(request.POST, instance=payroll)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.approved_by = request.user
            payroll.approved_at = timezone.now()
            payroll.save()
            messages.success(request, 'Payroll approved successfully.')
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollApprovalForm(instance=payroll)
    
    return render(request, 'payroll/payroll_approval.html', {
        'form': form,
        'payroll': payroll
    })

@login_required
def generate_payslip(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if payroll.status != 'approved':
        messages.error(request, 'Cannot generate payslip for unapproved payroll.')
        return redirect('payroll:payroll_detail', pk=payroll.pk)
    
    # Generate payslip logic here
    payslip = Payslip.objects.create(
        payroll_record=payroll,
        file='payslips/sample.pdf'  # Replace with actual file generation
    )
    
    messages.success(request, 'Payslip generated successfully.')
    return redirect('payroll:payroll_detail', pk=payroll.pk)

@login_required
def download_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    response = FileResponse(payslip.file, as_attachment=True)
    return response

@login_required
def monthly_payroll_report(request):
    """Generate monthly payroll report"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    payrolls = Payroll.objects.filter(
        month__month=month,
        month__year=year
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
        payrolls = payrolls.filter(month__gte=start_date)
    if end_date:
        payrolls = payrolls.filter(month__lte=end_date)
        
    return render(request, 'payroll/employee_report.html', {
        'payrolls': payrolls,
        'employee_id': employee_id,
        'start_date': start_date,
        'end_date': end_date
    })
