from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, 
    register, 
    profile, 
    update_profile,
    logout,
    protected_view,
    user_dashboard,
    admin_only_view
)

urlpatterns = [
    # Authentication endpoints
    path('register/', register, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('logout/', logout, name='logout'),
    
    # Protected route examples
    path('protected/', protected_view, name='protected_view'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('admin/', admin_only_view, name='admin_only_view'),
]
