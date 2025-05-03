from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'designation', 'is_staff')
    list_filter = ('role', 'department', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'marital_status')
    list_filter = ('gender', 'marital_status', 'nationality')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'emergency_contact_name')
    ordering = ('user__first_name', 'user__last_name')
