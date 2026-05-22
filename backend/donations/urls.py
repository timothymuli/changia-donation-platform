from django.urls import path
from .views import InitiateDonationView, MpesaCallbackView, DonationListView

urlpatterns = [
    path('donate/', InitiateDonationView.as_view(), name='donate'),
    path('callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('', DonationListView.as_view(), name='donation-list'),
]