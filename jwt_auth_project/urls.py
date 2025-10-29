from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Simple homepage view
def home(request):
    return JsonResponse({
        "message": "Welcome to the JWT Authentication API",
        "available_endpoints": {
            "auth": "/api/auth/",
            "protected": "/api/protected/",
            "weather": "/api/weather/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', home),  # 👈 Root URL now defined
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/protected/', include('authentication.urls')),  
    path('api/weather/', include('weather.urls')),
]
