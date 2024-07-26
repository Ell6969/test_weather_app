from django.test import Client, TestCase
from django.urls import reverse

from .models import SearchHistory


class WeatherViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('weather:index')
        self.history_url = reverse('weather:history')

    def test_index_post_request(self):
        # Отправляем POST-запрос с городом
        response = self.client.post(self.index_url, {'city': 'London'})
        self.assertEqual(response.status_code, 200)

        # Проверяем, что запись в SearchHistory была создана
        self.assertTrue(SearchHistory.objects.filter(city='London').exists())

    def test_index_get_request(self):
        # Установим значение в сессии
        self.client.cookies.load({'sessionid': 'fake-session-id'})
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather_card.html')
        # self.assertContains(response, 'Enter a city')

    def test_history_view(self):
        # Создаем историю поиска
        session_id = 'test-session-id'
        SearchHistory.objects.create(
            session_id=session_id,
            city='London',
            condition='Clear',
            temperature=25
        )
        self.client.cookies.load({'sessionid': session_id})
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/history.html')
        self.assertContains(response, 'London')
        self.assertContains(response, 'Clear')

    def test_most_popular_city_in_session(self):
        session_id = 'test-session-id'
        SearchHistory.objects.create(session_id=session_id, city='London', condition='Clear', temperature=25)
        SearchHistory.objects.create(session_id=session_id, city='New York', condition='Cloudy', temperature=15)
        # Создаем несколько записей для проверки
        SearchHistory.objects.create(session_id=session_id, city='London', condition='Clear', temperature=25)
        self.client.cookies.load({'sessionid': session_id})
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('most_popular_city', response.context)
        self.assertEqual(response.context['most_popular_city']['city'], 'London')
