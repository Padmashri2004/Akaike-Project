import requests
import json

url = "http://127.0.0.1:8000/classify"
data = {"input_email_body": "Hello, my email is john@example.com and phone is +919876543210"}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
