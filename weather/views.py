import requests
import json
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import WeatherSearch, SearchFilter
from .serializers import WeatherSearchSerializer, SearchFilterSerializer, WeatherSearchRequestSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather(request):
    city = request.GET.get('city')
    if not city:
        return Response({'error': 'City parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        return Response({'error': 'OpenWeatherMap API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        # OpenWeatherMap API call - try city name first
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)

        # If city not found (404), try with Bhutan country code for Bhutan cities
        if response.status_code == 404:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BT&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)

        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather data
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'country': data['sys']['country'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure'],
        }
        
        # Save search to database
        weather_search = WeatherSearch.objects.create(
            user=request.user,
            city=weather_data['city'],
            country=weather_data['country'],
            temperature=weather_data['temperature'],
            description=weather_data['description'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed'],
            pressure=weather_data['pressure']
        )
        
        return Response(weather_data, status=status.HTTP_200_OK)
        
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Weather API error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except KeyError as e:
        return Response({'error': f'Invalid weather data format: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_history(request):
    searches = WeatherSearch.objects.filter(user=request.user)[:10]  # Last 10 searches
    serializer = WeatherSearchSerializer(searches, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def advanced_search(request):
    """Advanced search functionality for weather data"""
    serializer = WeatherSearchRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    search_type = data.get('search_type', 'current')
    
    if search_type == 'current':
        # Search current weather for a city
        city = data.get('city')
        if not city:
            return Response({'error': 'City is required for current weather search'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Use existing get_weather logic
        return get_weather(request)
    
    elif search_type == 'history':
        # Search through user's search history
        queryset = WeatherSearch.objects.filter(user=request.user)
        
        # Apply filters
        if data.get('city'):
            queryset = queryset.filter(city__icontains=data['city'])
        
        if data.get('country'):
            queryset = queryset.filter(country__icontains=data['country'])
        
        if data.get('min_temperature') is not None:
            queryset = queryset.filter(temperature__gte=data['min_temperature'])
        
        if data.get('max_temperature') is not None:
            queryset = queryset.filter(temperature__lte=data['max_temperature'])
        
        if data.get('weather_condition'):
            queryset = queryset.filter(description__icontains=data['weather_condition'])
        
        searches = queryset[:20]  # Limit to 20 results
        serializer = WeatherSearchSerializer(searches, many=True)
        return Response(serializer.data)
    
    elif search_type == 'favorites':
        # Get user's favorite cities and show their current weather
        try:
            search_filter = SearchFilter.objects.get(user=request.user)
            favorite_cities = json.loads(search_filter.favorite_cities) if search_filter.favorite_cities else []
        except SearchFilter.DoesNotExist:
            favorite_cities = []
        
        if not favorite_cities:
            return Response({'message': 'No favorite cities set'}, status=status.HTTP_200_OK)
        
        results = []
        for city in favorite_cities[:5]:  # Limit to 5 favorites
            try:
                # Get current weather for favorite city
                api_key = settings.OPENWEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'country': data['sys']['country'],
                    'wind_speed': data['wind']['speed'],
                    'pressure': data['main']['pressure'],
                    'is_favorite': True
                }
                results.append(weather_data)
            except:
                continue  # Skip cities that fail
        
        return Response(results, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid search type'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def search_filters(request):
    """Manage user's search filters and preferences"""
    if request.method == 'GET':
        try:
            search_filter = SearchFilter.objects.get(user=request.user)
            serializer = SearchFilterSerializer(search_filter)
            return Response(serializer.data)
        except SearchFilter.DoesNotExist:
            return Response({'message': 'No search filters set'}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Create new search filter
        serializer = SearchFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        # Update existing search filter
        try:
            search_filter = SearchFilter.objects.get(user=request.user)
            serializer = SearchFilterSerializer(search_filter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SearchFilter.DoesNotExist:
            return Response({'error': 'Search filter not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_suggestions(request):
    """Get search suggestions based on user's history and popular searches"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response({'suggestions': []}, status=status.HTTP_200_OK)
    
    # Get user's recent searches
    user_searches = WeatherSearch.objects.filter(
        user=request.user,
        city__icontains=query
    ).values_list('city', flat=True).distinct()[:5]
    
    # Get popular searches across all users
    popular_searches = WeatherSearch.objects.filter(
        city__icontains=query
    ).values('city').annotate(
        count=Count('city')
    ).order_by('-count')[:5]
    
    suggestions = list(user_searches) + [item['city'] for item in popular_searches]
    suggestions = list(dict.fromkeys(suggestions))[:8]  # Remove duplicates and limit
    
    return Response({'suggestions': suggestions}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorites(request):
    """Manage user's favorite cities"""
    try:
        search_filter = SearchFilter.objects.get(user=request.user)
        favorite_cities = json.loads(search_filter.favorite_cities) if search_filter.favorite_cities else []
    except SearchFilter.DoesNotExist:
        search_filter = SearchFilter.objects.create(user=request.user)
        favorite_cities = []

    if request.method == 'GET':
        # Get current weather for favorite cities
        results = []
        for city in favorite_cities[:5]:  # Limit to 5 favorites
            try:
                api_key = settings.OPENWEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url, timeout=10)

                # If city not found (404), try with Bhutan country code for Bhutan cities
                if response.status_code == 404:
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BT&appid={api_key}&units=metric"
                    response = requests.get(url, timeout=10)

                response.raise_for_status()

                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'country': data['sys']['country'],
                    'wind_speed': data['wind']['speed'],
                    'pressure': data['main']['pressure'],
                    'is_favorite': True
                }
                results.append(weather_data)
            except:
                continue  # Skip cities that fail

        return Response(results, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        city = request.data.get('city')
        if not city:
            return Response({'error': 'City is required'}, status=status.HTTP_400_BAD_REQUEST)

        if city not in favorite_cities:
            favorite_cities.append(city)
            search_filter.favorite_cities = json.dumps(favorite_cities)
            search_filter.save()

        return Response({'message': f'{city} added to favorites'}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        city = request.data.get('city')
        if not city:
            return Response({'error': 'City is required'}, status=status.HTTP_400_BAD_REQUEST)

        if city in favorite_cities:
            favorite_cities.remove(city)
            search_filter.favorite_cities = json.dumps(favorite_cities)
            search_filter.save()
            return Response({'message': f'{city} removed from favorites'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'{city} not in favorites'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_analytics(request):
    """Get search analytics for the user"""
    user_searches = WeatherSearch.objects.filter(user=request.user)

    # Most searched cities
    popular_cities = user_searches.values('city').annotate(
        count=Count('city')
    ).order_by('-count')[:5]

    # Temperature distribution
    temp_ranges = {
        'cold': user_searches.filter(temperature__lt=10).count(),
        'cool': user_searches.filter(temperature__gte=10, temperature__lt=20).count(),
        'warm': user_searches.filter(temperature__gte=20, temperature__lt=30).count(),
        'hot': user_searches.filter(temperature__gte=30).count(),
    }

    # Weather conditions
    weather_conditions = user_searches.values('description').annotate(
        count=Count('description')
    ).order_by('-count')[:5]

    analytics = {
        'total_searches': user_searches.count(),
        'popular_cities': list(popular_cities),
        'temperature_distribution': temp_ranges,
        'weather_conditions': list(weather_conditions),
        'last_search': WeatherSearchSerializer(user_searches.first()).data if user_searches.exists() else None
    }

    return Response(analytics, status=status.HTTP_200_OK)
