import sqlite3
from rich.console import Console
from rich.table import Table

def get_ord1(cursor, parola):
    query = '''
        SELECT w.text, s.count 
        FROM sequences s
        JOIN words w ON s.target_id = w.id
        WHERE s.source_id = (SELECT id FROM words WHERE text = ?)
        ORDER BY s.count DESC LIMIT 3
    '''
    cursor.execute(query, (parola.lower(),))
    return cursor.fetchall()

def get_ord2(cursor, w1, w2):
    query = '''
        SELECT w3.text, COUNT(*) as frequenza
        FROM sequences s1
        JOIN words w2 ON s1.target_id = w2.id
        JOIN sequences s2 ON w2.id = s2.source_id
        JOIN words w3 ON s2.target_id = w3.id
        WHERE s1.source_id = (SELECT id FROM words WHERE text = ?)
        AND w2.text = ?
        GROUP BY w3.text
        ORDER BY frequenza DESC LIMIT 3
    '''
    cursor.execute(query, (w1.lower(), w2.lower()))
    return cursor.fetchall()

# Configurazione
conn = sqlite3.connect('iliade.db')
cursor = conn.cursor()
console = Console()

# Dati di test
input_1 = "achille"
input_2_a, input_2_b = "achille", "disse"

# Recupero dati
ris_ord1 = get_ord1(cursor, input_1)
ris_ord2 = get_ord2(cursor, input_2_a, input_2_b)
conn.close()

# Creazione Tabella
table = Table(title="Confronto Predizione: Ordine 1 vs Ordine 2")
table.add_column("Modello", style="cyan")
table.add_column("Input", style="magenta")
table.add_column("Output Predetti (Parola, Freq)")

table.add_row("Ordine 1", input_1, str(ris_ord1))
table.add_row("Ordine 2", f"{input_2_a} {input_2_b}", str(ris_ord2))

console.print(table)