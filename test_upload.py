import requests
import os

def test_file_upload():
    base_url = "http://localhost"
    
    # Test services endpoint
    print("1. Testing services endpoint...")
    response = requests.get(f"{base_url}/api/services")
    if response.status_code == 200:
        services = response.json()
        print("✅ Services loaded successfully")
        for service in services['services']:
            print(f"   - {service['name']}: {service['description']}")
    else:
        print("❌ Failed to load services")
        return
    
    # Test file upload for transcript service
    print("\n2. Testing file upload...")
    files = {
        'file': ('test_transcript.txt', open('test_transcript.txt', 'rb'), 'text/plain')
    }
    data = {
        'service_type': 'transcript_cleanup',
        'instructions': 'Please clean up this transcript file'
    }
    
    response = requests.post(f"{base_url}/api/files/upload", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ File upload successful!")
        print(f"   Order ID: {result['order_id']}")
        print(f"   File: {result['file_name']}")
        print(f"   Status: {result['status']}")
        
        # Test getting orders
        print("\n3. Testing orders endpoint...")
        response = requests.get(f"{base_url}/api/files/orders")
        if response.status_code == 200:
            orders = response.json()
            print("✅ Orders retrieved successfully")
            for order in orders['orders']:
                print(f"   - {order['id']}: {order['file_name']} ({order['status']})")
    else:
        print(f"❌ Upload failed: {response.text}")

if __name__ == "__main__":
    test_file_upload()
