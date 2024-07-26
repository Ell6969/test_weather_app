

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import SearchHistory
from .utils import get_session_id, get_weather


def index(request):
    session_id = get_session_id(request)
    most_popular_city = request.session.get('most_popular_city', None)

    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            # Получаем данные о погоде
            weather_data = get_weather(city)
            dt = timezone.now()

            if weather_data:
                condition_text = weather_data.get('current', {}).get('condition', {}).get('text', '')
                condition_icon = weather_data.get('current', {}).get('condition', {}).get('icon', '')
                temperatur = weather_data.get('current', {}).get('temp_c', '')

                response_data = {
                    'city': city,
                    'temperature': temperatur,
                    'condition_text': condition_text,
                    'condition_icon': condition_icon,
                    'date': dt.strftime('%Y-%m-%d'),
                    'time': dt.strftime('%H:%M:%S'),
                }
                SearchHistory.objects.create(
                    session_id=session_id,
                    city=city,
                    condition=condition_text,
                    temperature=temperatur,
                )
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Could not fetch weather data'}, status=500)
        else:
            return JsonResponse({'error': 'City not provided'}, status=400)

    return render(request, 'weather/weather_card.html', {'most_popular_city': most_popular_city})


def history(request):
    session_id = get_session_id(request)
    search_history = SearchHistory.objects.filter(session_id=session_id)

    city_counts = search_history.values('city').annotate(count=Count('city')).order_by('-count')
    most_popular_city = city_counts.first() if city_counts.exists() else None

    if most_popular_city:
        request.session['most_popular_city'] = most_popular_city

    return render(request, 'weather/history.html', {
        'search_history': search_history,
        'city_counts': city_counts,
        'most_popular_city': most_popular_city,
    })
