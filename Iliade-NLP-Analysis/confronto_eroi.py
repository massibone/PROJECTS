import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def get_dati_eroe(cursor, eroe):
    query = '''
        SELECT w.text, s.count 
        FROM sequences s
        JOIN words w ON s.target_id = w.id
        WHERE s.source_id = (SELECT id FROM words WHERE text = ?)
        AND w.pos IN ('VERB', 'NOUN', 'ADJ')
        ORDER BY s.count DESC LIMIT 5
    '''
    cursor.execute(query, (eroe.lower(),))
    return dict(cursor.fetchall())

# Connessione al DB
conn = sqlite3.connect('iliade.db')
cursor = conn.cursor()

eroi = ['achille', 'ettore', 'ulisse']
dati_confronto = {eroe: get_dati_eroe(cursor, eroe) for eroe in eroi}
conn.close()

# Preparazione Grafico
fig, ax = plt.subplots(figsize=(12, 7))
colori = {'achille': 'red', 'ettore': 'blue', 'ulisse': 'green'}

# Creazione barre raggruppate
all_words = set()
for eroe in eroi:
    all_words.update(dati_confronto[eroe].keys())
parole_etichette = list(all_words)

indice = np.arange(len(parole_etichette))
larghezza = 0.25

for i, eroe in enumerate(eroi):
    # Creiamo una lista di frequenze allineata alle parole_etichette
    frequenze = [dati_confronto[eroe].get(p, 0) for p in parole_etichette]
    
    ax.bar(indice + (i * larghezza), frequenze, larghezza, label=eroe.capitalize(), color=colori[eroe])

ax.set_title('Confronto Lessicale: Cosa segue i protagonisti?', fontsize=14)
ax.set_xticks(indice + larghezza)
ax.set_xticklabels(parole_etichette, rotation=45) # Ora il numero di tick e label coincide
ax.set_ylabel('Frequenza')
ax.legend()
plt.tight_layout()
plt.show()