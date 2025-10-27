"""
JWT Authentication API Test Script

This script demonstrates how to use the JWT authentication API endpoints.
Run this script to test the JWT authentication system.

Usage:
    python test_jwt_api.py

Make sure the Django development server is running:
    python manage.py runserver
"""

import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://localhost:8000/api/auth"

# ANSI colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_section(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def register_user():
    """Test user registration"""
    print_section("1. USER REGISTRATION")
    
    test_data = {
        "username": f"testuser_{hash(__file__) % 10000}",
        "email": f"test_{hash(__file__) % 10000}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    print(f"Registering user: {test_data['username']}")
    
    try:
        response = requests.post(f"{BASE_URL}/register/", json=test_data)
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"User registered successfully!")
            print(f"  Username: {test_data['username']}")
            print(f"  Email: {test_data['email']}")
            return test_data['username'], test_data['password']
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to the server. Is it running?")
        print_info("Start the server with: python manage.py runserver")
        return None, None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None, None


def login(username, password):
    """Test user login"""
    print_section("2. USER LOGIN")
    
    print(f"Logging in as: {username}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login successful!")
            print(f"  Access Token: {data['access'][:50]}...")
            print(f"  Refresh Token: {data['refresh'][:50]}...")
            return data['access'], data['refresh']
        else:
            print_error(f"Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None, None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None, None


def get_profile(access_token):
    """Test getting user profile"""
    print_section("3. GET USER PROFILE")
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Profile retrieved successfully!")
            print(f"  Username: {data['username']}")
            print(f"  Email: {data['email']}")
            print(f"  First Name: {data.get('first_name', 'N/A')}")
            print(f"  Last Name: {data.get('last_name', 'N/A')}")
            return True
        else:
            print_error(f"Failed to get profile: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_protected_endpoint(access_token):
    """Test protected endpoint"""
    print_section("4. TEST PROTECTED ENDPOINT")
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/protected/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Protected endpoint accessed successfully!")
            print(f"  Message: {data['message']}")
            print(f"  User ID: {data['user_id']}")
            return True
        else:
            print_error(f"Failed to access protected endpoint: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_dashboard(access_token):
    """Test dashboard endpoint"""
    print_section("5. TEST DASHBOARD")
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Dashboard accessed successfully!")
            print(f"  Message: {data['message']}")
            if 'dashboard_data' in data:
                print(f"  Status: {data['dashboard_data']['account_status']}")
            return True
        else:
            print_error(f"Failed to access dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def refresh_token(refresh_token_value):
    """Test token refresh"""
    print_section("6. REFRESH TOKEN")
    
    try:
        response = requests.post(
            f"{BASE_URL}/token/refresh/",
            json={"refresh": refresh_token_value}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Token refreshed successfully!")
            print(f"  New Access Token: {data['access'][:50]}...")
            return data['access']
        else:
            print_error(f"Token refresh failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None


def logout(access_token):
    """Test logout"""
    print_section("7. LOGOUT")
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{BASE_URL}/logout/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Logout successful!")
            print(f"  Message: {data['message']}")
            return True
        else:
            print_error(f"Logout failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    """Main test function"""
    print(f"\n{Colors.BOLD}JWT Authentication API Test Suite{Colors.END}")
    print(f"{Colors.BOLD}Base URL: {BASE_URL}{Colors.END}\n")
    
    # Check if server is running
    try:
        requests.get("http://localhost:8000", timeout=2)
        print_success("Server is running")
    except:
        print_error("Server is not running. Please start it with 'python manage.py runserver'")
        sys.exit(1)
    
    # Test registration
    username, password = register_user()
    if not username or not password:
        print_error("\nTest suite failed - could not register user")
        sys.exit(1)
    
    # Test login
    access_token, refresh_token_value = login(username, password)
    if not access_token:
        print_error("\nTest suite failed - could not login")
        sys.exit(1)
    
    # Test profile
    if not get_profile(access_token):
        print_warning("Profile test failed, continuing...")
    
    # Test protected endpoint
    if not test_protected_endpoint(access_token):
        print_warning("Protected endpoint test failed, continuing...")
    
    # Test dashboard
    if not test_dashboard(access_token):
        print_warning("Dashboard test failed, continuing...")
    
    # Test token refresh
    if refresh_token_value:
        new_access_token = refresh_token(refresh_token_value)
        if new_access_token:
            print_info("Using new access token for logout test")
            access_token = new_access_token
    
    # Test logout
    logout(access_token)
    
    # Summary
    print_section("TEST SUMMARY")
    print_success("All tests completed!")
    print(f"\n{Colors.BOLD}Test Credentials:{Colors.END}")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"\nYou can use these credentials to test the API manually.")
    print(f"Or use the access token to make authenticated requests.")
    

if __name__ == "__main__":
    main()


