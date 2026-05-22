from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'target_amount', 'amount_raised', 'status', 'deadline', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'creator__username']