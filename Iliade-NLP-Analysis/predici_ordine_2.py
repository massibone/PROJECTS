import sqlite3
import matplotlib.pyplot as plt

def visualizza_predizioni(parola_input):
    conn = sqlite3.connect('iliade.db')
    cursor = conn.cursor()
   
    # Query che filtra per categorie grammaticali significative (Nomi, Verbi, Aggettivi)
    query = '''
        SELECT w.text, s.count
        FROM sequences s
        JOIN words w ON s.target_id = w.id
        WHERE s.source_id = (SELECT id FROM words WHERE text = ?)
        AND w.pos IN ('NOUN', 'VERB', 'ADJ')
        ORDER BY s.count DESC LIMIT 10
    '''
    cursor.execute(query, (parola_input.lower(),))
    dati = cursor.fetchall()
    conn.close()

    if not dati:
        print("Nessun dato significativo trovato.")
        return

    # Preparazione dati per Matplotlib
    parole = [r[0] for r in dati]
    frequenze = [r[1] for r in dati]

    # Creazione grafico
    plt.figure(figsize=(10, 6))
    plt.bar(parole, frequenze, color='teal', edgecolor='black')
    plt.title(f"Parole più frequenti dopo '{parola_input}' (Analisi di Tesi)")
    plt.xlabel("Parola successiva")
    plt.ylabel("Frequenza")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
   
    # Mostra grafico
    plt.tight_layout()
    plt.show()

# Esempio di utilizzo
visualizza_parola = "achille"
print(f"Generazione grafico per: {visualizza_parola}...")
visualizza_predizioni(visualizza_parola)
