import sqlite3
import spacy

# Percorso al modello locale (modifica se necessario)
MODEL_PATH = r"C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\Iliade_Neo4j_Spacy\modello_spacy\it_core_news_sm\it_core_news_sm-3.8.0"
nlp = spacy.load(MODEL_PATH)

def init_db():
    conn = sqlite3.connect('iliade.db')
    cursor = conn.cursor()
    # Tabella per le parole uniche
    cursor.execute('CREATE TABLE IF NOT EXISTS words (id INTEGER PRIMARY KEY, text TEXT UNIQUE, lemma TEXT, pos TEXT)')
    # Tabella per le relazioni di successione
    cursor.execute('CREATE TABLE IF NOT EXISTS sequences (source_id INTEGER, target_id INTEGER, count INTEGER)')
    conn.commit()
    return conn

def process_text(file_path, conn):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
   
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_punct and not token.is_space]
   
    cursor = conn.cursor()
   
    # 1. Inserisci le parole uniche nel DB
    for token in tokens:
        cursor.execute('INSERT OR IGNORE INTO words (text, lemma, pos) VALUES (?, ?, ?)',
                       (token.text.lower(), token.lemma_, token.pos_))
    conn.commit()
   
    # 2. Crea le sequenze (bigrammi)
    for i in range(len(tokens) - 1):
        w1, w2 = tokens[i].text.lower(), tokens[i+1].text.lower()
       
        # Recupera gli ID
        cursor.execute('SELECT id FROM words WHERE text = ?', (w1,))
        s_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM words WHERE text = ?', (w2,))
        t_id = cursor.fetchone()[0]
       
        # Aggiorna la frequenza della sequenza
        cursor.execute('INSERT OR REPLACE INTO sequences (source_id, target_id, count) VALUES (?, ?, COALESCE((SELECT count FROM sequences WHERE source_id=? AND target_id=?)+1, 1))',
                       (s_id, t_id, s_id, t_id))
    conn.commit()

# Esecuzione
conn = init_db()
process_text('data/Iliade.txt', conn)
print("Analisi completata e database popolato!")
conn.close()
