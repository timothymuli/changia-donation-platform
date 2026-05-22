from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Campaign
from .serializers import CampaignSerializer
from logs.utils import create_log

class CampaignListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaigns = Campaign.objects.filter(creator=request.user)
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.save(creator=request.user)
            create_log(request.user, 'CREATE_CAMPAIGN', f'Campaign created: {campaign.title}')
            return Response({
                'message': 'Campaign created successfully',
                'campaign': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampaignDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Campaign.objects.get(pk=pk, creator=user)
        except Campaign.DoesNotExist:
            return None

    def get(self, request, pk):
        campaign = self.get_object(pk, request.user)
        if not campaign:
            return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data)

    def put(self, request, pk):
        campaign = self.get_object(pk, request.user)
        if not campaign:
            return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CampaignSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_log(request.user, 'UPDATE_CAMPAIGN', f'Campaign updated: {campaign.title}')
            return Response({
                'message': 'Campaign updated successfully',
                'campaign': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        campaign = self.get_object(pk, request.user)
        if not campaign:
            return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
        create_log(request.user, 'DELETE_CAMPAIGN', f'Campaign deleted: {campaign.title}')
        campaign.delete()
        return Response({'message': 'Campaign deleted successfully'}, status=status.HTTP_204_NO_CONTENT)