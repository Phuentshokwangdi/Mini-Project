from django.db import models
from django.conf import settings  


class WeatherSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ fix here
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    humidity = models.IntegerField()
    wind_speed = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"


class SearchFilter(models.Model):
    """Model to store user's search preferences and filters"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    min_temperature = models.FloatField(null=True, blank=True)
    max_temperature = models.FloatField(null=True, blank=True)
    weather_conditions = models.CharField(max_length=500, blank=True)  # JSON string of conditions
    favorite_cities = models.CharField(max_length=1000, blank=True)  # JSON string of cities
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user']

    def __str__(self):
        return f"Search filters for {self.user.username}"
