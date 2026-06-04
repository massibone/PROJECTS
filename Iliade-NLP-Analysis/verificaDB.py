import sqlite3

conn = sqlite3.connect('iliade.db')
cursor = conn.cursor()

# Conta quante parole uniche abbiamo
cursor.execute('SELECT COUNT(*) FROM words')
print(f"Parole totali uniche nel database: {cursor.fetchone()[0]}")

# Conta quante sequenze (bigrammi) abbiamo
cursor.execute('SELECT COUNT(*) FROM sequences')
print(f"Relazioni di successione totali: {cursor.fetchone()[0]}")

cursor.execute('''
    SELECT w.text, s.count 
    FROM sequences s
    JOIN words w ON s.target_id = w.id
    WHERE s.source_id = (SELECT id FROM words WHERE text = 'achille')
    ORDER BY s.count DESC LIMIT 10
''')
print(cursor.fetchall())

cursor.execute('''
    SELECT w.text, s.count 
    FROM sequences s
    JOIN words w ON s.target_id = w.id
    WHERE s.source_id = (SELECT id FROM words WHERE text = 'achille')
    AND w.pos IN ('NOUN', 'VERB', 'ADJ')  -- Solo Nomi, Verbi, Aggettivi
    ORDER BY s.count DESC LIMIT 10
''')
print(cursor.fetchall())

conn.close()