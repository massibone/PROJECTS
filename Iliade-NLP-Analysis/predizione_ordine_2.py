'''
Dato che hai già il database con le singole parole, 
il modo più rapido per farlo senza dover ricostruire tutto 
è utilizzare una Self-Join su SQLite. In pratica, 
chiediamo al database di trovare una parola A, 
poi la parola B che segue A, 
e infine la parola C che segue B.
'''
import sqlite3
import matplotlib.pyplot as plt

def predici_con_trigramma(w1, w2):
    conn = sqlite3.connect('iliade.db')
    cursor = conn.cursor()
    
    # Cerchiamo la parola C che segue la sequenza W1 -> W2
    # In SQLite, cerchiamo: W1 -> W2 AND W2 -> W3
    query = '''
        SELECT w3.text, COUNT(*) as frequenza
        FROM sequences s1
        JOIN words w2 ON s1.target_id = w2.id
        JOIN sequences s2 ON w2.id = s2.source_id
        JOIN words w3 ON s2.target_id = w3.id
        WHERE s1.source_id = (SELECT id FROM words WHERE text = ?)
        AND w2.text = ?
        AND w3.pos IN ('NOUN', 'VERB', 'ADJ')
        GROUP BY w3.text
        ORDER BY frequenza DESC LIMIT 5
    '''
    cursor.execute(query, (w1.lower(), w2.lower()))
    dati = cursor.fetchall()
    conn.close()
    return dati

# Test: Cosa dice Achille?
w1, w2 = "achille", "disse"
risultati = predici_con_trigramma(w1, w2)

if risultati:
    print(f"Dopo la sequenza '{w1} {w2}', le parole più frequenti sono:")
    for parola, freq in risultati:
        print(f"- {parola}: {freq}")
else:
    print(f"Nessuna sequenza trovata per '{w1} {w2}'")