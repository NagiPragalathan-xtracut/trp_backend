import requests
import json

def send_webhook_data():
    # Webhook URL
    url = "https://integrationcloud-in21.leadsquaredapps.com/v1/webhook/lsq/76003/115/1818c91d-e217-4dbc-afbb-5bd54d5bf414/b3f28134-ea35-4363-86e0-81e447a514ea/7d7883dd-d885-44a9-8ca6-9c2f9dd83178"
    
    # Query parameters
    params = {
        "ickey": "f00519f0ab66d40b368b0888b232c66c6f76a907e88df154f93426373276b553c34cbadf886422e427b52c3b7620de76d025a8c0638a2bf9e484bdc1e1c66c3335a70d8ce8e0fa467c8e6b84e0950077a7281cd2af5b59461a3470df788e5524c47b4a75497f6b37"
    }
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "firstName": "nagipragalathan",
        "mobileNo": "6379065405",
        "email": "gokul@xtracut.com",
        "location": "chennai"
    }

    try:
        # Make the POST request
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload
        )
        
        # Print the response
        print("Status Code:", response.status_code)
        print("Response:")
        print(json.dumps(response.json(), indent=4))
        
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    send_webhook_data() 