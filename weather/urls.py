from django.urls import path
from .views import (
    get_weather, weather_history, advanced_search,
    search_filters, search_suggestions, search_analytics, favorites
)

urlpatterns = [
    path('', get_weather, name='get_weather'),
    path('history/', weather_history, name='weather_history'),
    path('search/', advanced_search, name='advanced_search'),
    path('filters/', search_filters, name='search_filters'),
    path('suggestions/', search_suggestions, name='search_suggestions'),
    path('analytics/', search_analytics, name='search_analytics'),
    path('favorites/', favorites, name='favorites'),
]
