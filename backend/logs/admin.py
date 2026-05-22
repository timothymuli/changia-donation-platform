from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'details', 'created_at']
    list_filter = ['action']
    search_fields = ['user__username', 'action']