import requests
from datetime import datetime

API_KEY = "P35Q6ZDPJU3FQR3NRP9BPZCFA5V6V1YMRR"
today = datetime.utcnow().strftime("%Y-%m-%d")

params = {
    "module": "stats",
    "action": "dailyavggasprice",
    "startdate": today,
    "enddate": today,
    "apikey": API_KEY
}

r = requests.get("https://api.basescan.org/api", params=params)
print("Request URL:", r.url)
print("Response JSON:", r.text)

data = r.json()
if data.get("status") == "1":
    for entry in data["result"]:
        print(f"{entry['UTCDate']}: {int(entry['averagegasprice'])/1e9} Gwei")
else:
    print("❌ API Error:", data.get("message"), "| data:", data)
