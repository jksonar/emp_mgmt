from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import PerformanceReview, PerformanceGoal
from .forms import PerformanceReviewForm, PerformanceFeedbackForm, PerformanceGoalForm, PerformanceGoalUpdateForm

@login_required
def review_list(request):
    """List all performance reviews"""
    reviews = PerformanceReview.objects.all()
    return render(request, 'performance/review_list.html', {'reviews': reviews})

@login_required
def review_create(request):
    """Create a new performance review"""
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.employee = request.user.employee
            review.save()
            return redirect('performance:review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm()
    return render(request, 'performance/review_form.html', {'form': form})

@login_required
def review_detail(request, pk):
    """View performance review details"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    return render(request, 'performance/review_detail.html', {'review': review})

@login_required
def review_update(request, pk):
    """Update performance review"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('performance:review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm(instance=review)
    return render(request, 'performance/review_form.html', {'form': form})

@login_required
def review_submit(request, pk):
    """Submit a performance review"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        review.status = 'submitted'
        review.submitted_at = timezone.now()
        review.save()
        return redirect('performance:review_detail', pk=review.pk)
    return render(request, 'performance/review_submit.html', {'review': review})

@login_required
def review_feedback(request, pk):
    """Provide feedback for a performance review"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        form = PerformanceFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.review = review
            feedback.given_by = request.user
            feedback.save()
            return redirect('performance:review_detail', pk=review.pk)
    else:
        form = PerformanceFeedbackForm()
    return render(request, 'performance/review_feedback.html', {'form': form, 'review': review})

@login_required
def goal_list(request):
    """List all performance goals"""
    goals = PerformanceGoal.objects.all()
    return render(request, 'performance/goal_list.html', {'goals': goals})

@login_required
def goal_create(request):
    """Create a new performance goal"""
    if request.method == 'POST':
        form = PerformanceGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.employee = request.user.employee
            goal.save()
            return redirect('performance:goal_detail', pk=goal.pk)
    else:
        form = PerformanceGoalForm()
    return render(request, 'performance/goal_form.html', {'form': form})

@login_required
def goal_detail(request, pk):
    """View performance goal details"""
    goal = get_object_or_404(PerformanceGoal, pk=pk)
    return render(request, 'performance/goal_detail.html', {'goal': goal})

@login_required
def goal_update(request, pk):
    """Update performance goal"""
    goal = get_object_or_404(PerformanceGoal, pk=pk)
    if request.method == 'POST':
        form = PerformanceGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('performance:goal_detail', pk=goal.pk)
    else:
        form = PerformanceGoalForm(instance=goal)
    return render(request, 'performance/goal_form.html', {'form': form})

@login_required
def goal_progress_update(request, pk):
    """Update goal progress"""
    goal = get_object_or_404(PerformanceGoal, pk=pk)
    if request.method == 'POST':
        form = PerformanceGoalUpdateForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save()
            return redirect('performance:goal_detail', pk=goal.pk)
    else:
        form = PerformanceGoalUpdateForm(instance=goal)
    return render(request, 'performance/goal_progress_form.html', {'form': form, 'goal': goal})
