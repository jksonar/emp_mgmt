from django.contrib import admin

# Register your models here.
from .models import Department, Designation

admin.site.register(Department)
admin.site.register(Designation)
