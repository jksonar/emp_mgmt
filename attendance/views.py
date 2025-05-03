from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Attendance, AttendanceCorrection
from .forms import AttendanceForm, AttendanceCorrectionForm

@login_required
def attendance_list(request):
    """List all attendance records"""
    attendances = Attendance.objects.all()
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_mark(request):
    """Mark attendance for an employee"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = request.user.employee
            attendance.save()
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form})

@login_required
def attendance_detail(request, pk):
    """View attendance details"""
    attendance = get_object_or_404(Attendance, pk=pk)
    return render(request, 'attendance/attendance_detail.html', {'attendance': attendance})

@login_required
def attendance_update(request, pk):
    """Update attendance details"""
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance:attendance_detail', pk=attendance.pk)
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'attendance/attendance_form.html', {'form': form})

@login_required
def correction_list(request):
    """List all attendance corrections"""
    corrections = AttendanceCorrection.objects.all()
    return render(request, 'attendance/correction_list.html', {'corrections': corrections})

@login_required
def correction_create(request):
    """Create a new attendance correction"""
    if request.method == 'POST':
        form = AttendanceCorrectionForm(request.POST)
        if form.is_valid():
            correction = form.save(commit=False)
            correction.employee = request.user.employee
            correction.save()
            return redirect('attendance:correction_list')
    else:
        form = AttendanceCorrectionForm()
    return render(request, 'attendance/correction_form.html', {'form': form})

@login_required
def correction_detail(request, pk):
    """View correction details"""
    correction = get_object_or_404(AttendanceCorrection, pk=pk)
    return render(request, 'attendance/correction_detail.html', {'correction': correction})

@login_required
def correction_approve(request, pk):
    """Approve an attendance correction"""
    correction = get_object_or_404(AttendanceCorrection, pk=pk)
    if request.method == 'POST':
        correction.status = 'approved'
        correction.approved_by = request.user
        correction.approved_at = timezone.now()
        correction.save()
        return redirect('attendance:correction_detail', pk=correction.pk)
    return render(request, 'attendance/correction_approve.html', {'correction': correction})

@login_required
def daily_report(request):
    """Generate daily attendance report"""
    date = request.GET.get('date', timezone.now().date())
    attendances = Attendance.objects.filter(date=date)
    return render(request, 'attendance/daily_report.html', {
        'date': date,
        'attendances': attendances
    })

@login_required
def monthly_report(request):
    """Generate monthly attendance report"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    attendances = Attendance.objects.filter(
        date__month=month,
        date__year=year
    )
    return render(request, 'attendance/monthly_report.html', {
        'month': month,
        'year': year,
        'attendances': attendances
    })

@login_required
def employee_report(request):
    """Generate employee-specific attendance report"""
    employee_id = request.GET.get('employee_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    attendances = Attendance.objects.all()
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
        
    return render(request, 'attendance/employee_report.html', {
        'attendances': attendances,
        'employee_id': employee_id,
        'start_date': start_date,
        'end_date': end_date
    })
