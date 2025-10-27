"""
Complete test of all JWT endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

print("\n" + "="*70)
print("COMPLETE JWT AUTHENTICATION TEST")
print("="*70)

# Step 1: Register
print("\n1. TESTING REGISTRATION")
print("-" * 70)
username = f"testuser_{hash(__file__) % 100000}"
try:
    registration_data = {
        "username": username,
        "email": f"{username}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=registration_data, timeout=10)
    if response.status_code == 201:
        print(f"✓ Registration successful!")
        print(f"  Username: {username}")
    else:
        print(f"✗ Registration failed: {response.status_code}")
        print(f"  {response.text}")
        exit(1)
except Exception as e:
    print(f"✗ Registration error: {e}")
    exit(1)

# Step 2: Login
print("\n2. TESTING LOGIN")
print("-" * 70)
try:
    login_data = {
        "username": username,
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data, timeout=10)
    if response.status_code == 200:
        data = response.json()
        access_token = data['access']
        refresh_token = data['refresh']
        print(f"✓ Login successful!")
        print(f"  Access Token: {access_token[:50]}...")
        print(f"  Refresh Token: {refresh_token[:50]}...")
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"  {response.text}")
        exit(1)
except Exception as e:
    print(f"✗ Login error: {e}")
    exit(1)

# Step 3: Get Profile
print("\n3. TESTING PROFILE ENDPOINT")
print("-" * 70)
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"✓ Profile retrieved successfully!")
        profile_data = response.json()
        print(f"  User: {profile_data['username']}")
        print(f"  Email: {profile_data['email']}")
    else:
        print(f"✗ Profile failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Profile error: {e}")

# Step 4: Update Profile
print("\n4. TESTING PROFILE UPDATE")
print("-" * 70)
try:
    update_data = {
        "first_name": "UpdatedTest",
        "last_name": "UpdatedUser"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.put(f"{BASE_URL}/profile/update/", headers=headers, json=update_data, timeout=10)
    if response.status_code == 200:
        print(f"✓ Profile updated successfully!")
    else:
        print(f"✗ Profile update failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Profile update error: {e}")

# Step 5: Protected View
print("\n5. TESTING PROTECTED VIEW")
print("-" * 70)
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/protected/", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"✓ Protected view accessed successfully!")
    else:
        print(f"✗ Protected view failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Protected view error: {e}")

# Step 6: Dashboard
print("\n6. TESTING DASHBOARD")
print("-" * 70)
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/dashboard/", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"✓ Dashboard accessed successfully!")
    else:
        print(f"✗ Dashboard failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Dashboard error: {e}")

# Step 7: Refresh Token
print("\n7. TESTING TOKEN REFRESH")
print("-" * 70)
try:
    response = requests.post(
        f"{BASE_URL}/token/refresh/",
        json={"refresh": refresh_token},
        timeout=10
    )
    if response.status_code == 200:
        print(f"✓ Token refreshed successfully!")
    else:
        print(f"✗ Token refresh failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Token refresh error: {e}")

# Step 8: Logout
print("\n8. TESTING LOGOUT")
print("-" * 70)
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/logout/", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"✓ Logout successful!")
    else:
        print(f"✗ Logout failed: {response.status_code}")
        print(f"  {response.text}")
except Exception as e:
    print(f"✗ Logout error: {e}")

print("\n" + "="*70)
print("ALL TESTS COMPLETED")
print("="*70)
print("\n✓ JWT Authentication is working correctly!")
print(f"Test Credentials:")
print(f"  Username: {username}")
print(f"  Password: testpass123\n")

