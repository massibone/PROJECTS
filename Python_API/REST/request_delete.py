# elimina una risorsa con una richiesta DELETE.

import requests

response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)

