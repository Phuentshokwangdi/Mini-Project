from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user profile
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout user (in a real implementation, you might want to blacklist the token)
    """
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


# Protected route examples
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Example of a protected view that requires authentication
    """
    return Response({
        'message': f'Hello {request.user.username}! This is a protected view.',
        'user_id': request.user.id,
        'user_email': request.user.email,
        'timestamp': request.user.date_joined
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """
    Example dashboard view for authenticated users
    """
    return Response({
        'message': 'Welcome to your dashboard!',
        'user': UserSerializer(request.user).data,
        'dashboard_data': {
            'total_logins': 1,  # This would come from a real tracking system
            'last_login': request.user.last_login,
            'account_status': 'Active' if request.user.is_active else 'Inactive'
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_only_view(request):
    """
    Example view that requires admin privileges
    """
    if not request.user.is_staff:
        return Response({
            'error': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    return Response({
        'message': 'Admin panel access granted',
        'admin_user': request.user.username,
        'admin_data': {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'staff_users': User.objects.filter(is_staff=True).count()
        }
    })

