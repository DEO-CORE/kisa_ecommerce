from django.test import TestCase
from rest_framework.test import APIClient
from .models import Subscriber


class SubscriptionTests(TestCase):
    def test_subscription_is_saved_without_duplicates(self):
        client = APIClient()
        for _ in range(2):
            response = client.post('/api/newsletter/subscribe/', {'email': 'test@example.com'}, format='json')
            self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertEqual(client.post('/api/newsletter/subscribe/', {'email': 'wrong'}, format='json').status_code, 400)
