Monitoraggio prezzi
Configurazione Email: Definisci le impostazioni per inviare notifiche via email quando il prezzo scende.
Funzioni di Prezzo:
get_price_amazon e get_price_ebay: Funzioni per ottenere il prezzo del prodotto. Dovrai completare l'integrazione con le rispettive API.
Notifica Prezzo:
La funzione notify_price_drop controlla se il nuovo prezzo è inferiore del 10% rispetto al prezzo precedente. In caso affermativo, invia una notifica.
Registrazione Prezzi:
record_price salva il prezzo attuale in un file CSV.
Main:
Raccoglie i prezzi da Amazon e eBay, salva i dati e invia notifiche se necessario.
