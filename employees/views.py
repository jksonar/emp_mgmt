from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser, UserProfile, Document, WorkHistory
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, DocumentForm, WorkHistoryForm
from django.contrib.auth import login, logout, authenticate

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = self.object.documents.all()
        context['work_history'] = self.object.work_history.all()
        return context

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

@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('employees:document_list')

@login_required
def work_history_list(request):
    work_history = request.user.work_history.all()
    return render(request, 'employees/work_history_list.html', {'work_history': work_history})

@login_required
def work_history_create(request):
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST)
        if form.is_valid():
            work_history = form.save(commit=False)
            work_history.user = request.user
            work_history.save()
            messages.success(request, 'Work history added successfully.')
            return redirect('employees:work_history_list')
    else:
        form = WorkHistoryForm()
    
    return render(request, 'employees/work_history_form.html', {'form': form})

@login_required
def work_history_update(request, pk):
    work_history = get_object_or_404(WorkHistory, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST, instance=work_history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work history updated successfully.')
            return redirect('employees:work_history_list')
    else:
        form = WorkHistoryForm(instance=work_history)
    
    return render(request, 'employees/work_history_form.html', {'form': form})

@login_required
def work_history_delete(request, pk):
    work_history = get_object_or_404(WorkHistory, pk=pk, user=request.user)
    work_history.delete()
    messages.success(request, 'Work history deleted successfully.')
    return redirect('employees:work_history_list')

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
