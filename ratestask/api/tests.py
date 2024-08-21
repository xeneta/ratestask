from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Port, Price, Region


class PriceViewSetTests(APITestCase):
    def setUp(self):
        # Create test data
        self.region = Region.objects.create(slug='region1', name='Region 1')
        self.port1 = Port.objects.create(code='P001', name='Port 1', parent_slug=self.region)
        self.port2 = Port.objects.create(code='P002', name='Port 2', parent_slug=self.region)
        self.price1 = Price.objects.create(
            day=datetime.now().date() - timedelta(days=1),
            price=100,
            orig_code=self.port1,
            dest_code=self.port2
        )
        self.price2 = Price.objects.create(
            day=datetime.now().date(),
            price=150,
            orig_code=self.port1,
            dest_code=self.port2
        )
        self.url = reverse('price-average-prices')


    def test_missing_parameters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Missing parameters"})

    def test_invalid_date_format(self):
        response = self.client.get(self.url, {'date_from': '2024-08-32', 'date_to': '2024-08-30', 'origin': 'P001', 'destination': 'P002'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Invalid date format. Use YYYY-MM-DD."})

    def test_date_greater_than_current_date(self):
        future_date = (datetime.now() + timedelta(days=1)).date()
        response = self.client.get(self.url, {'date_from': '2024-08-01', 'date_to': future_date, 'origin': 'P001', 'destination': 'P002'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "The 'date_to' parameter cannot be greater than the current date."})
