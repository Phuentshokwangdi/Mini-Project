from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock
from .models import WeatherSearch

User = get_user_model()


class WeatherSearchModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_weather_search(self):
        weather_search = WeatherSearch.objects.create(
            user=self.user,
            city='London',
            temperature=15.5,
            description='Cloudy',
            humidity=70
        )
        self.assertEqual(weather_search.city, 'London')
        self.assertEqual(weather_search.temperature, 15.5)
        self.assertEqual(weather_search.user, self.user)


class WeatherAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    @patch('weather.views.requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock the OpenWeatherMap API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'London',
            'main': {
                'temp': 15.5,
                'humidity': 70,
                'pressure': 1013
            },
            'weather': [{'description': 'cloudy'}],
            'sys': {'country': 'GB'},
            'wind': {'speed': 5.2}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = reverse('get_weather')
        response = self.client.get(url, {'city': 'London'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'London')
        self.assertEqual(response.data['temperature'], 15.5)
        self.assertEqual(response.data['humidity'], 70)

    def test_get_weather_no_city(self):
        url = reverse('get_weather')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weather_history(self):
        # Create some weather searches
        WeatherSearch.objects.create(
            user=self.user,
            city='London',
            temperature=15.5,
            description='Cloudy',
            humidity=70
        )
        WeatherSearch.objects.create(
            user=self.user,
            city='Paris',
            temperature=18.0,
            description='Sunny',
            humidity=60
        )

        url = reverse('weather_history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['city'], 'Paris')  # Most recent first
