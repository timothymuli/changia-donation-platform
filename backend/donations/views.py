from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Donation
from .serializers import DonationSerializer
from campaigns.models import Campaign
import requests
import base64
from datetime import datetime
from django.conf import settings


def get_mpesa_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    response = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"}
    )
    return response.json().get("access_token")


def get_mpesa_password():
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
    return password, timestamp


class InitiateDonationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        campaign_id = request.data.get('campaign_id')
        phone = request.data.get('phone')
        amount = request.data.get('amount')

        try:
            campaign = Campaign.objects.get(id=campaign_id, status='active')
        except Campaign.DoesNotExist:
            return Response({'error': 'Campaign not found or not active'}, status=status.HTTP_404_NOT_FOUND)

        donation = Donation.objects.create(
            campaign=campaign,
            donor_phone=phone,
            amount=amount,
            status='pending'
        )

        try:
            token = get_mpesa_token()
            password, timestamp = get_mpesa_password()

            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(float(amount)),
                "PartyA": phone,
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": phone,
                "CallBackURL": settings.MPESA_CALLBACK_URL,
                "AccountReference": f"Changia-{campaign_id}",
                "TransactionDesc": f"Donation to {campaign.title}"
            }

            response = requests.post(
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

            response_data = response.json()

            if response_data.get("ResponseCode") == "0":
                return Response({
                    'message': 'STK push sent to your phone, enter your PIN to complete donation',
                    'donation_id': donation.id,
                    'checkout_request_id': response_data.get('CheckoutRequestID')
                })
            else:
                donation.status = 'failed'
                donation.save()
                return Response({'error': 'Failed to initiate payment'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            donation.status = 'failed'
            donation.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.get('Body', {}).get('stkCallback', {})
        result_code = data.get('ResultCode')
        checkout_request_id = data.get('CheckoutRequestID')

        try:
            donation = Donation.objects.get(transaction_id=checkout_request_id)
        except Donation.DoesNotExist:
            return Response({'message': 'ok'})

        if result_code == 0:
            donation.status = 'successful'
            campaign = donation.campaign
            campaign.amount_raised += donation.amount
            campaign.save()
        else:
            donation.status = 'failed'

        donation.save()
        return Response({'message': 'ok'})


class DonationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaigns = Campaign.objects.filter(creator=request.user)
        donations = Donation.objects.filter(campaign__in=campaigns)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
