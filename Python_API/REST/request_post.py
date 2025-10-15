# invia una richiesta POST con dati JSON
import requests

data = {'title': 'foo', 'body': 'bar', 'userId': 1}
response = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
print(response.json())
