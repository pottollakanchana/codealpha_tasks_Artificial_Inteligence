import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
# Suppress TensorFlow warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from music21 import converter, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras import Input
from tensorflow.keras.utils import to_categorical
import glob

print("🔥 MUSIC GENERATOR STARTED")

# =========================
# 1. LOAD MIDI FILES
# =========================
notes = []

print("Loading MIDI files from: dataset")

for file in glob.glob("dataset/*.mid"):
    print(f"Reading: {file}")
    midi = converter.parse(file)
    
    # FIXED: .flat → .flatten()
    elements = midi.flatten().notes

    for element in elements:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

print(f"Total notes loaded: {len(notes)}")

# =========================
# 2. PREPARE DATA
# =========================
sequence_length = 100

pitchnames = sorted(set(notes))
n_vocab = len(pitchnames)

note_to_int = {note: number for number, note in enumerate(pitchnames)}

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    
    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

# reshape input
network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(n_vocab)

network_output = to_categorical(network_output)

# =========================
# 3. BUILD MODEL (FIXED)
# =========================
model = Sequential([
    Input(shape=(network_input.shape[1], network_input.shape[2])),
    
    LSTM(256, return_sequences=True),
    Dropout(0.3),
    
    LSTM(256),
    Dense(256, activation='relu'),
    Dropout(0.3),
    
    Dense(n_vocab, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam')

# =========================
# 4. TRAIN MODEL
# =========================
print("Training model...")
model.fit(network_input, network_output, epochs=10, batch_size=32)

# =========================
# 5. GENERATE MUSIC
# =========================
print("Generating music...")

start = np.random.randint(0, len(network_input) - 1)
pattern = network_input[start]

prediction_output = []

int_to_note = {number: note for number, note in enumerate(pitchnames)}

for _ in range(200):  # length of generated notes
    prediction_input = np.reshape(pattern, (1, len(pattern), 1))
    
    prediction = model.predict(prediction_input, verbose=0)
    index = np.argmax(prediction)
    
    result = int_to_note[index]
    prediction_output.append(result)

    pattern = np.append(pattern, index / float(n_vocab))
    pattern = pattern[1:]

# =========================
# 6. SAVE MIDI FILE
# =========================
offset = 0
output_notes = []

for pattern in prediction_output:
    if '.' in pattern:
        notes_in_chord = pattern.split('.')
        chord_notes = []

        for n in notes_in_chord:
            new_note = note.Note(int(n))
            new_note.offset = offset
            chord_notes.append(new_note)

        new_chord = chord.Chord(chord_notes)
        output_notes.append(new_chord)

    else:
        new_note = note.Note(pattern)
        new_note.offset = offset
        output_notes.append(new_note)

    offset += 0.5

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='output.mid')

print("✅ DONE! output.mid created")