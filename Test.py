import requests

url = "http://127.0.0.1:8000/summarize"
data = {
    "text": "In recent years, the rapid advancement of artificial intelligence (AI) and machine learning (ML) has revolutionized multiple industries, transforming the way businesses operate, people interact, and data is processed.",
    "max_length": 800,
    "min_length": 40,
    "num_beams": 4
}
response = requests.post(url, json=data)
print(response.json())