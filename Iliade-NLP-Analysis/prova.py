import spacy

# Carica il modello puntando direttamente alla cartella estratta
model_path = r"C:\Users\D79197\OneDrive - Comune di FIRENZE\Documenti\PYTHON_PROJECT\broadcastSite\Iliade_Neo4j_Spacy\modello_spacy\it_core_news_sm\it_core_news_sm-3.8.0"

try:
    nlp = spacy.load(model_path)
    print("Modello caricato con successo!")
   
    # Un piccolo test per verificare che sia tutto OK
    doc = nlp("L'ira funesta di Achille.")
    print("Analisi completata:", [token.text for token in doc])
   
except Exception as e:
    print(f"Qualcosa non va ancora: {e}")
