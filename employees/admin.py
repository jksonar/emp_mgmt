from django.contrib import admin
from .models import CustomUser, UserProfile, Document, WorkHistory
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(WorkHistory)

