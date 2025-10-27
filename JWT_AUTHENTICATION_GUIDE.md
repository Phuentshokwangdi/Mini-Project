# JWT Authentication Guide

This document provides comprehensive information about the JWT (JSON Web Token) authentication system implemented in this project.

## Overview

The project uses `djangorestframework-simplejwt` for JWT-based authentication. This provides a secure and stateless authentication mechanism for the REST API.

## Configuration

### Settings (weather_portal/settings.py)

```python
# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
**POST** `/api/auth/register/`

Creates a new user account.

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "message": "User created successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2024-01-01T00:00:00Z",
        "is_active": true
    }
}
```

#### 2. User Login (Obtain JWT Tokens)
**POST** `/api/auth/login/`

Authenticates a user and returns access and refresh tokens.

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Claims:**
- `username`
- `email`
- `first_name`
- `last_name`
- `user_id`
- `exp` (expiration time)
- `iat` (issued at time)

#### 3. Refresh Access Token
**POST** `/api/auth/token/refresh/`

Refreshes the access token using the refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. Get User Profile
**GET** `/api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2024-01-01T00:00:00Z",
    "is_active": true
}
```

#### 5. Update User Profile
**PUT** `/api/auth/profile/update/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "first_name": "Johnny",
    "last_name": "Smith",
    "email": "johnny@example.com"
}
```

**Response (200 OK):**
```json
{
    "message": "Profile updated successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "johnny@example.com",
        "first_name": "Johnny",
        "last_name": "Smith",
        "date_joined": "2024-01-01T00:00:00Z",
        "is_active": true
    }
}
```

#### 6. Logout
**POST** `/api/auth/logout/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Logged out successfully"
}
```

### Protected Endpoints

#### 1. Protected View
**GET** `/api/auth/protected/`

Example protected endpoint that requires authentication.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Hello john_doe! This is a protected view.",
    "user_id": 1,
    "user_email": "john@example.com",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 2. User Dashboard
**GET** `/api/auth/dashboard/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Welcome to your dashboard!",
    "user": {...},
    "dashboard_data": {
        "total_logins": 1,
        "last_login": null,
        "account_status": "Active"
    }
}
```

#### 3. Admin Only View
**GET** `/api/auth/admin/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK) - Admin:**
```json
{
    "message": "Admin panel access granted",
    "admin_user": "admin",
    "admin_data": {
        "total_users": 10,
        "active_users": 8,
        "staff_users": 2
    }
}
```

**Response (403 Forbidden) - Non-Admin:**
```json
{
    "error": "Admin access required"
}
```

## Using JWT Tokens

### Making Authenticated Requests

Include the access token in the `Authorization` header:

```http
GET /api/weather/?city=London HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### JavaScript Example

```javascript
// Login function
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    // Store tokens
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    
    return data;
}

// Make authenticated request
async function getWeather(city) {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch(`http://localhost:8000/api/weather/?city=${city}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}

// Refresh token when expired
async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh })
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    
    return data;
}
```

### Python Example (using requests)

```python
import requests

# Login
login_url = "http://localhost:8000/api/auth/login/"
login_data = {
    "username": "john_doe",
    "password": "securepassword123"
}

response = requests.post(login_url, json=login_data)
tokens = response.json()

access_token = tokens['access']
refresh_token = tokens['refresh']

# Make authenticated request
headers = {
    "Authorization": f"Bearer {access_token}"
}

weather_url = "http://localhost:8000/api/weather/"
params = {"city": "London"}
response = requests.get(weather_url, headers=headers, params=params)
weather_data = response.json()

# Refresh token
refresh_url = "http://localhost:8000/api/auth/token/refresh/"
refresh_data = {"refresh": refresh_token}
response = requests.post(refresh_url, json=refresh_data)
new_tokens = response.json()
```

### cURL Examples

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'

# Get profile
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get weather (protected endpoint)
curl -X GET "http://localhost:8000/api/weather/?city=London" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Refresh token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

## Token Management

### Token Lifetimes

- **Access Token**: 60 minutes (configurable)
- **Refresh Token**: 7 days (configurable)

### Token Rotation

When `ROTATE_REFRESH_TOKENS` is enabled, each time you refresh an access token, you get a new refresh token. The old refresh token is automatically blacklisted.

### Token Blacklist

The project includes token blacklist functionality to immediately revoke tokens:

```python
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

# Get user's tokens
user = request.user
tokens = OutstandingToken.objects.filter(user=user)

# Blacklist all tokens for a user
for token in tokens:
    BlacklistedToken.objects.create(token=token)
```

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Token Storage**: Store tokens securely (httpOnly cookies, secure local storage)
3. **Token Expiration**: Configure appropriate expiration times
4. **Token Rotation**: Enable token rotation to reduce security risks
5. **CORS**: Configure CORS appropriately for your frontend origins
6. **Password Strength**: Implement strong password requirements
7. **Rate Limiting**: Consider implementing rate limiting on authentication endpoints

## Testing JWT Endpoints

### Using Django REST Framework Browsable API

1. Start the development server: `python manage.py runserver`
2. Navigate to `http://localhost:8000/api/auth/`
3. Use the browsable API to test endpoints

### Using Postman/Insomnia

1. Create a collection for the API
2. Add environment variables for tokens
3. Use the environment variables in Authorization headers

### Using Python Test Framework

```python
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_login(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_protected_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/auth/protected/')
        self.assertEqual(response.status_code, 200)
```

## Migration Commands

Run these commands to set up the database:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations (including token blacklist tables)
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Troubleshooting

### "Token is expired"
- Use the refresh endpoint to get a new access token
- Or login again to get new tokens

### "Token is blacklisted"
- The token has been intentionally revoked
- Login again to get new tokens

### "Authentication credentials were not provided"
- Ensure the Authorization header is included: `Authorization: Bearer <token>`

### "Invalid token"
- Check if the token format is correct
- Ensure the token hasn't been tampered with
- Verify the JWT_SECRET_KEY matches

## Additional Resources

- [djangorestframework-simplejwt Documentation](https://djangorestframework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decode and verify JWT tokens
- [Django REST Framework](https://www.django-rest-framework.org/)

