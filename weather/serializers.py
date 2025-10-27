from rest_framework import serializers
from .models import WeatherSearch, SearchFilter
import json


class WeatherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSearch
        fields = ['id', 'city', 'country', 'temperature', 'description', 'humidity', 'wind_speed', 'pressure', 'searched_at']
        read_only_fields = ['id', 'searched_at']


class SearchFilterSerializer(serializers.ModelSerializer):
    weather_conditions = serializers.SerializerMethodField()
    favorite_cities = serializers.SerializerMethodField()

    class Meta:
        model = SearchFilter
        fields = ['id', 'min_temperature', 'max_temperature', 'weather_conditions', 'favorite_cities', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_weather_conditions(self, obj):
        if obj.weather_conditions:
            try:
                return json.loads(obj.weather_conditions)
            except json.JSONDecodeError:
                return []
        return []

    def get_favorite_cities(self, obj):
        if obj.favorite_cities:
            try:
                return json.loads(obj.favorite_cities)
            except json.JSONDecodeError:
                return []
        return []

    def create(self, validated_data):
        # Handle JSON fields
        weather_conditions = self.initial_data.get('weather_conditions', [])
        favorite_cities = self.initial_data.get('favorite_cities', [])
        
        validated_data['weather_conditions'] = json.dumps(weather_conditions)
        validated_data['favorite_cities'] = json.dumps(favorite_cities)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle JSON fields
        weather_conditions = self.initial_data.get('weather_conditions', instance.weather_conditions)
        favorite_cities = self.initial_data.get('favorite_cities', instance.favorite_cities)
        
        if isinstance(weather_conditions, list):
            validated_data['weather_conditions'] = json.dumps(weather_conditions)
        if isinstance(favorite_cities, list):
            validated_data['favorite_cities'] = json.dumps(favorite_cities)
        
        return super().update(instance, validated_data)


class WeatherSearchRequestSerializer(serializers.Serializer):
    """Serializer for advanced weather search requests"""
    city = serializers.CharField(max_length=100, required=False)
    min_temperature = serializers.FloatField(required=False)
    max_temperature = serializers.FloatField(required=False)
    weather_condition = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)
    search_type = serializers.ChoiceField(choices=['current', 'history', 'favorites'], default='current')
