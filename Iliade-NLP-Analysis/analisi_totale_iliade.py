'''
Generazione di grafici statici informativi con Matplotlib per visualizzare:
Frequenza delle parole
Distribuzione del grado
Clustering coefficient
Probabilità previste per la parola successiva
Altri grafici a discrezione per visualizzare le informazioni del grafo e del modello
Risultati attesi
'''
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

def get_word_text(cursor, word_id):
    """Recupera il testo della parola dato il suo ID."""
    cursor.execute("SELECT text FROM words WHERE id = ?", (word_id,))
    result = cursor.fetchone()
    return result[0] if result else str(word_id)

def analizza_iliade():
    conn = sqlite3.connect('iliade.db')
    cursor = conn.cursor()
    
    # 1. Caricamento Grafo
    G = nx.DiGraph()
    cursor.execute("SELECT source_id, target_id, count FROM sequences")
    for src, tgt, weight in cursor.fetchall():
        G.add_edge(src, tgt, weight=weight)

    # 2. Calcolo Metriche
    degrees = [d for n, d in G.degree()]
    clustering = nx.clustering(G.to_undirected())
    pagerank = nx.pagerank(G, weight='weight')
    
    # --- NUOVO FILTRO STOP-WORDS ---
    stop_words = {'il', 'la', 'i', 'gli', 'le', 'a', 'di', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'e', 'che', 'o', 'non', 'si', 'del', 'della', 'dei', 'delle'}
    
    # Filtriamo il dizionario pagerank rimuovendo le chiavi (ID) che corrispondono alle stop-words
    filtered_pagerank = {}
    for node_id, score in pagerank.items():
        text = get_word_text(cursor, node_id)
        if text.lower() not in stop_words and len(text) > 2: # Escludiamo anche parole cortissime
            filtered_pagerank[node_id] = score
    # -------------------------------
    
    # 3. Preparazione dati (usiamo filtered_pagerank invece di pagerank)
    top_ids = sorted(filtered_pagerank, key=filtered_pagerank.get, reverse=True)[:10]
    top_words = [get_word_text(cursor, i) for i in top_ids]
    top_values = [filtered_pagerank[i] for i in top_ids]
    
    conn.close()

    # 4. Visualizzazione
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Grafico A: Distribuzione del Grado
    axs[0, 0].hist(degrees, bins=50, color='skyblue', log=True)
    axs[0, 0].set_title("Distribuzione del Grado (Scala Log)")

    # Grafico B: Clustering Coefficient
    axs[0, 1].hist(list(clustering.values()), bins=30, color='salmon')
    axs[0, 1].set_title("Coefficiente di Clustering")

    # Grafico C: Top 10 Parole (PageRank)
    axs[1, 0].barh(top_words[::-1], top_values[::-1], color='mediumseagreen')
    axs[1, 0].set_title("Top 10 Parole Hub (PageRank)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analizza_iliade()

# Esecuzione
if __name__ == "__main__":
    analizza_iliade()
'''
piegazione per la tua Tesi:
Distribuzione del Grado: Se il grafico appare come una "curva che scende verso destra", stai dimostrando che l'Iliade segue la legge di potenza (Power Law). È una proprietà tipica dei sistemi complessi e del linguaggio umano: poche parole sono usate tantissimo (hub), moltissime sono usate raramente.

Clustering Coefficient: Ti permette di affermare che il linguaggio omerico è "strutturato in cluster". Indica che le parole non appaiono in modo casuale, ma in gruppi semantici coesi.

PageRank: È l'algoritmo di Google. Identifica le parole che "tengono insieme" la rete narrativa. È un modo molto solido per estrarre il "lessico fondamentale" del testo analizzato.

Nota: Per visualizzare i nomi delle parole nel grafico del PageRank (al posto dei numeri ID), dovresti fare un'ulteriore query per mappare i 10 ID top_words con la tabella words. Vuoi che aggiungiamo questa funzione di "traduzione ID-Testo" per avere i nomi veri nel grafico?
'''
'''
Ho aggiunto una funzione helper get_word_text che interroga il database per recuperare il termine leggibile partendo dall'ID, rendendo il grafico del PageRank immediatamente comprensibile per la tua tesi.
'''