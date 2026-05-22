from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    amount_raised = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'target_amount', 'amount_raised', 'deadline', 'status', 'creator', 'created_at']