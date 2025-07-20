import mido
import time
import random
from music21 import stream, instrument, note, converter


# Apri un porta MIDI virtuale
#out_port = mido.open_output('My virtual port')

# Definisci una scala
scale = [60, 62, 64, 65, 67, 69, 71]

# Crea una funzione per suonare una nota
def play_note(note, duration):
    message = mido.Message('note_on', note=note, velocity=100)
    #out_port.send(message)
    time.sleep(duration)
    message = mido.Message('note_off', note=note, velocity=100)
    #out_port.send(message)

# Matrice di probabilità di transizione (più dettagliata)
transition_matrix = {
    "C2-C3": {"C3-C4": 0.7, "D2-D3": 0.2, "C2-C3": 0.1},
    # ... altre transizioni
}

def generate_note(current_region, previous_note):
    """
    Genera la prossima nota in base alla regione corrente e alla nota precedente.

    Args:
        current_region (str): La regione musicale corrente.
        previous_note (int): La nota musicale precedente.

    Returns:
        int: La prossima nota musicale.
    """

    if current_region not in transition_matrix:
        return 60
        #raise ValueError(f"La regione '{current_region}' non è presente nella matrice di transizione.")

    # Scegli la prossima regione in base alle probabilità e all'intervallo
    possible_next_regions = transition_matrix[current_region]
    intervals = {region: abs(note - previous_note) for region, note in possible_next_regions.items()}
    weighted_probs = {region: prob / sum(intervals.values()) for region, prob in possible_next_regions.items()}
    next_region = random.choices(list(weighted_probs.keys()), weights=list(weighted_probs.values()))[0]

    # Scegli una nota casuale nella regione (esempio semplificato)
    start_note, end_note = current_region.split('-')
    start_note = int(start_note.replace('C', '')) * 12
    end_note = int(end_note.replace('C', '')) * 12
    next_note = random.randint(start_note, end_note)

    return next_note

# Inizia la generazione della melodia
current_region = "C4-C5"
previous_note = 60  # Do centrale
melody = []
for _ in range(100):
    next_note = generate_note(current_region, previous_note)
    melody.append(next_note)
    play_note(next_note, 0.5)
    previous_note = next_note


# Create a Music21 Stream
stream1 = stream.Stream()
piano = instrument.Piano()
stream1.insert(0, piano)

# Add notes to the stream
for note_value in melody:
    note_object = note.Note(note_value)
    stream1.append(note_object)

# Write the stream to a MIDI file
stream1.write('midi', fp='output.mid')

# Convert MIDI to MP3 (you can use tools like ffmpeg or online converters)
# For example, using the command line:
# ffmpeg -i output.mid output.mp3
