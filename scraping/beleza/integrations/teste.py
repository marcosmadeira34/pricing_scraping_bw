import requests

url = "https://api.plugg.to/oauth/token"

payload = "client_id=3fc1e08b248f23a635916902750fc1f6&client_secret=7d7ae938accebc643b4deac7e03c91f3&username=1636404074924&password=cm9nZXJpby5jYXNhZG9Ab3V0bG9vay5jb20uYnIwLjc4MDkzNjY0NTEyNTc1NTMxNjM2NDA0MDc0OTI0&grant_type=password"
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)


