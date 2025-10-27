"""
Test only login endpoint with detailed error handling
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

print("\n" + "="*60)
print("TESTING LOGIN ENDPOINT")
print("="*60)

# Test Login
print("\nAttempting login...")
try:
    login_data = {
        "username": "testuser123",
        "password": "testpass123"
    }
    
    response = requests.post(
        f"{BASE_URL}/login/", 
        json=login_data, 
        timeout=15,
        allow_redirects=False
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    try:
        data = response.json()
        print(f"Response Data: {json.dumps(data, indent=2)}")
    except:
        print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        print("✓ Login successful!")
    else:
        print("✗ Login failed!")
        
except requests.exceptions.Timeout:
    print("✗ Request timed out. The server may be busy or stuck.")
except requests.exceptions.ConnectionError:
    print("✗ Could not connect to server. Is it running?")
    print("   Start server with: python manage.py runserver")
except Exception as e:
    print(f"✗ Error: {str(e)}")
    print(f"   Error Type: {type(e).__name__}")

print("\n" + "="*60)


