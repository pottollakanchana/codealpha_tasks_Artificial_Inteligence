from music21 import stream, note
import os

os.makedirs("dataset", exist_ok=True)

def create_midi(filename):
    s = stream.Stream()

    # Enough notes for training (IMPORTANT FIX)
    notes = ["C4","D4","E4","F4","G4","A4","B4","C5"] * 20

    for n in notes:
        s.append(note.Note(n))

    s.write("midi", fp=f"dataset/{filename}")

create_midi("song1.mid")
create_midi("song2.mid")
create_midi("song3.mid")

print("Dataset created successfully!")