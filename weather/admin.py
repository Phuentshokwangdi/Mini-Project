from django.contrib import admin
from .models import WeatherSearch

@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'temperature', 'description', 'humidity', 'searched_at']
    list_filter = ['searched_at', 'city']
    search_fields = ['city', 'user__username']
    readonly_fields = ['searched_at']
