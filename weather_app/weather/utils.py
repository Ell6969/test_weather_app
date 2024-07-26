import requests
from django.conf import settings

api_key = settings.API_KEY_WEATHER


def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_weather(city):
    api_key = '13884ef6fa014caaaae122254242007'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
