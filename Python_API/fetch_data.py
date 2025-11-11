# Recupera dati da un’API e salvare il risultato in un DataFrame df

from data_utils import fetch_data

# Recupera i dati dall'API
df = fetch_data('https://api.example.com/data')

# Stampa le prime righe del DataFrame per verificare il contenuto
print(df.head())
