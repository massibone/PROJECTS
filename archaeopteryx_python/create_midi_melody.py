import random
from music21 import stream, note, duration, instrument

def create_midi_melody():
    """
    Genera una melodia MIDI casuale basata su una scala estesa .
    """
    # Crea un nuovo stream musicale
    melody_stream = stream.Stream()
    
    # Aggiungi un pianoforte come strumento
    piano = instrument.Piano()
    melody_stream.append(piano)
    
    # --- SEZIONE MODIFICATA ---
    # Definisci una scala di Do maggiore su tre ottave.
    # I numeri sono i valori MIDI delle note. Il Do centrale (C4) è 60.
    
    # Ottava bassa (Do3 - Si3)
    ottava_bassa = [48, 50, 52, 53, 55, 57, 59]
    
    # Ottava centrale (Do4 - Si4)
    ottava_centrale = [60, 62, 64, 65, 67, 69, 71]
    
    # Ottava alta (Do5 - Do6)
    ottava_alta = [72, 74, 76, 77, 79, 81, 83, 84]

    # Unisci tutte le ottave per creare la scala completa
    scale = ottava_bassa + ottava_centrale + ottava_alta
    
   

    # Parametri della melodia
    num_notes = 64  # Aumentato il numero di note per una melodia più lunga
    possible_durations = [0.25, 0.5, 1, 1.5] # Aggiunta la durata da 0.25 (croma)
    
    # Genera la melodia
    for _ in range(num_notes):
        # Scegli una nota casuale dalla scala estesa
        pitch_midi = random.choice(scale)
        
        # Scegli una durata casuale
        note_duration = random.choice(possible_durations)
        
        # Crea una nuova nota usando il valore MIDI
        new_note = note.Note(pitch_midi)
        new_note.duration = duration.Duration(note_duration)
        new_note.volume.velocity = random.randint(60, 100)  # Volume casuale
        
        # Aggiungi la nota allo stream
        melody_stream.append(new_note)
            
    return melody_stream


def save_midi(filename="melodia_estesa.mid"):
    """
    Salva la melodia generata come file MIDI.
    """
    try:
        # Crea e salva la melodia
        melody = create_midi_melody()
        melody.write('midi', fp=filename)
        print(f"File MIDI salvato come: {filename}")
        
        print("\nPer convertire il MIDI in MP3 puoi utilizzare un convertitore online.")
        
    except Exception as e:
        print(f"Errore durante il salvataggio del file MIDI: {e}")


# Esegui il programma
if __name__ == "__main__":
    # Assicurati di avere installato music21 con: pip install music21
    # Potrebbe essere necessario configurare il percorso di un software
    # di notazione musicale come MuseScore per alcune funzionalità avanzate,
    # ma per il salvataggio MIDI non è richiesto.
    save_midi()

