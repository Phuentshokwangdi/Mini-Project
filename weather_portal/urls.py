from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/weather/', include('weather.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
