from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_phone', 'campaign', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['status']
    search_fields = ['donor_phone', 'transaction_id']
