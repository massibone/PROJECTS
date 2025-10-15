# aggiorna una risorsa esistente con una richiesta PUT
import requests

data = {'title': 'foo', 'body': 'bar', 'userId': 1}
response = requests.put('https://jsonplaceholder.typicode.com/posts/1', json=data)
print(response.json())
