"""
Quick test script for registration and login
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

print("\n" + "="*60)
print("TESTING REGISTRATION AND LOGIN")
print("="*60)

# Test Registration
print("\n1. Testing Registration...")
try:
    registration_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=registration_data, timeout=5)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("   ✓ Registration successful!")
    else:
        print(f"   ✗ Registration failed!")
        
except requests.exceptions.ConnectionError:
    print("   ✗ Could not connect to server. Is it running?")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

# Test Login
print("\n2. Testing Login...")
try:
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data, timeout=5)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Login successful!")
        print(f"   Access Token: {data.get('access', 'N/A')[:50]}...")
        print(f"   Refresh Token: {data.get('refresh', 'N/A')[:50]}...")
        
        # Test Profile
        print("\n3. Testing Protected Endpoint (Profile)...")
        headers = {"Authorization": f"Bearer {data['access']}"}
        profile_response = requests.get(f"{BASE_URL}/profile/", headers=headers, timeout=5)
        print(f"   Status Code: {profile_response.status_code}")
        if profile_response.status_code == 200:
            print(f"   ✓ Profile retrieved: {json.dumps(profile_response.json(), indent=2)}")
        else:
            print(f"   ✗ Profile failed: {profile_response.text}")
    else:
        print(f"   ✗ Login failed!")
        print(f"   Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("   ✗ Could not connect to server. Is it running?")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)


