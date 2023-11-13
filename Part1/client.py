import requests

response = requests.get("http://127.0.0.1:8000/my-first-api?name=jacob")

print(response.status_code)
print(response.json())
