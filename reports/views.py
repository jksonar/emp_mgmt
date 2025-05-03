from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from employees.models import CustomUser, Department
from attendance.models import Attendance
from leave.models import LeaveApplication, LeaveBalance
from payroll.models import Payroll
from performance.models import PerformanceReview, PerformanceGoal
import csv
from datetime import datetime

@login_required
def employee_directory(request):
    """Generate employee directory report"""
    employees = CustomUser.objects.filter(role='employee')
    return render(request, 'reports/employee_directory.html', {'employees': employees})

@login_required
def department_employees(request):
    """Generate department-wise employee report"""
    departments = Department.objects.all()
    return render(request, 'reports/department_employees.html', {'departments': departments})

@login_required
def attrition_report(request):
    """Generate employee attrition report"""
    # Get employees who left in the last year
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    attritions = CustomUser.objects.filter(
        date_of_leaving__gte=one_year_ago,
        date_of_leaving__lte=timezone.now(),
        role='employee'
    )
    return render(request, 'reports/attrition_report.html', {'attritions': attritions})

@login_required
def attendance_daily_report(request):
    """Generate daily attendance report"""
    date = request.GET.get('date', timezone.now().date())
    attendances = Attendance.objects.filter(date=date)
    return render(request, 'reports/attendance_daily_report.html', {
        'date': date,
        'attendances': attendances
    })

@login_required
def attendance_monthly_report(request):
    """Generate monthly attendance report"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    attendances = Attendance.objects.filter(
        date__month=month,
        date__year=year
    )
    return render(request, 'reports/attendance_monthly_report.html', {
        'month': month,
        'year': year,
        'attendances': attendances
    })

@login_required
def attendance_employee_report(request):
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
        
    return render(request, 'reports/attendance_employee_report.html', {
        'attendances': attendances,
        'employee_id': employee_id,
        'start_date': start_date,
        'end_date': end_date
    })

@login_required
def leave_balance_report(request):
    """Generate leave balance report"""
    balances = LeaveBalance.objects.all()
    return render(request, 'reports/leave_balance_report.html', {'balances': balances})

@login_required
def leave_usage_report(request):
    """Generate leave usage report"""
    leaves = LeaveApplication.objects.filter(status='approved')
    return render(request, 'reports/leave_usage_report.html', {'leaves': leaves})

@login_required
def payroll_monthly_report(request):
    """Generate monthly payroll report"""
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    payrolls = Payroll.objects.filter(
        month__month=month,
        month__year=year
    )
    return render(request, 'reports/payroll_monthly_report.html', {
        'month': month,
        'year': year,
        'payrolls': payrolls
    })

@login_required
def payroll_employee_report(request):
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
        
    return render(request, 'reports/payroll_employee_report.html', {
        'payrolls': payrolls,
        'employee_id': employee_id,
        'start_date': start_date,
        'end_date': end_date
    })

@login_required
def performance_review_report(request):
    """Generate performance review report"""
    reviews = PerformanceReview.objects.all()
    return render(request, 'reports/performance_review_report.html', {'reviews': reviews})

@login_required
def performance_goal_report(request):
    """Generate performance goal report"""
    goals = PerformanceGoal.objects.all()
    return render(request, 'reports/performance_goal_report.html', {'goals': goals})

@login_required
def export_employees(request):
    """Export employee data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Department', 'Designation', 'Email', 'Phone', 'Joining Date'])
    
    employees = CustomUser.objects.filter(role='employee')
    for employee in employees:
        writer.writerow([
            employee.employee_id,
            employee.get_full_name(),
            employee.department.name if employee.department else '',
            employee.designation.name if employee.designation else '',
            employee.email,
            employee.phone_number,
            employee.date_of_joining
        ])
    
    return response

@login_required
def export_attendance(request):
    """Export attendance data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Date', 'Status', 'Check In', 'Check Out'])
    
    attendances = Attendance.objects.all()
    for attendance in attendances:
        writer.writerow([
            attendance.employee.employee_id,
            attendance.employee.user.get_full_name(),
            attendance.date,
            attendance.status,
            attendance.check_in,
            attendance.check_out
        ])
    
    return response

@login_required
def export_leave(request):
    """Export leave data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leave.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Leave Type', 'Start Date', 'End Date', 'Status'])
    
    leaves = LeaveApplication.objects.all()
    for leave in leaves:
        writer.writerow([
            leave.employee.employee_id,
            leave.employee.user.get_full_name(),
            leave.leave_type.name,
            leave.start_date,
            leave.end_date,
            leave.status
        ])
    
    return response

@login_required
def export_payroll(request):
    """Export payroll data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payroll.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Name', 'Month', 'Basic Salary', 'Status'])
    
    payrolls = Payroll.objects.all()
    for payroll in payrolls:
        writer.writerow([
            payroll.employee.employee_id,
            payroll.employee.get_full_name(),
            payroll.month,
            payroll.basic_salary,
            payroll.status
        ])
    
    return response
