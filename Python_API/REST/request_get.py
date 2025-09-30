import requests


#Questo esempio invia una richiesta GET a un endpoint REST e stampa la risposta JSON.

response = requests.get('https://jsonplaceholder.typicode.com/posts')
print(response.json())



