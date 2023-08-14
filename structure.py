import datetime as d
import os
import traceback

ALLNOTES = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

IONIAN = [0, 2, 4, 5, 7, 9, 11]

CHORD_DETAILS = dict([("ø", "Same as: -7 b5"), ("+", "Augmented")])

ASCII_PIANO = [
" ___________________________________________________________________________________ ",
"|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |",
"|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |",
"|  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |",
"|  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |  |_| |_|  |  |_| |_| |_|  |",
"|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
"|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
"|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|",
]
ASCII_WHITES = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35]

WHITE_FILL = "░"
BLACK_FILL = "█"

class Key:
    def __init__(self, root) :
        self.root = root
        self.shifted_notes = self.shift_to_root(root)

    def shift_to_root(self, root):
        root_index = ALLNOTES.index(root)
        return ALLNOTES[root_index:] + ALLNOTES[:root_index]

    def get_ionian(self):
        return [self.shifted_notes[i] for i in IONIAN]
        
class Chord:
    def __init__(self, root, chord):
        try:
            self.root = root
            self.key = Key(root)
            parts = chord.split()
            self.base = parts[0]
            self.modifiers = parts[1:]
            self.schema = self.build_schema()
            self.notes = self.get_notes() 
            self.keyboard = self.to_string()
        except Exception as e:
            file_path = os.path.join("./logs", f"error-{d.datetime.utcnow().isoformat()}")
            with open(file_path, 'w') as file:
                file.write(f"for the following root {root} and chord {chord}\n{e}\n{traceback.format_exc()}")
            raise e
    
    def build_schema(self):
        CHORD_BASES = dict([
            ("ø", ["1" , "b3" , "b5" , "b7"]),
            ("o", ["1" , "b3" , "b5" , "bb7"]),
            ("-", ["1" , "b3" , "5"]),
            ("+", ["1" , "3" , "#5"]),
            ("sus4", ["1", "4", "5"]),
        ])
        schema = ["1" , "3" , "5"]
        hasFlats = True
        schema_base = self.base
        if "△" in schema_base:
            hasFlats = False
            schema_base = schema_base.replace("△", "")
        for base in CHORD_BASES.keys():
            if base in schema_base:
                schema = CHORD_BASES.get(base)
                schema_base = schema_base.replace(base, "")
                break
            
        if schema_base:
            
            def append_flat_if_needed(i):
                return f"{'b' if hasFlats and i < 9 else ''}{str(i)}"
            
            # add all the dominant notes in the chord base
            for i in range(7, int(schema_base) + 1, 2):
                schema.append(append_flat_if_needed(i))
                
            # will add a sixth if it is present in the chord base
            if schema_base == "6":
                schema.append(append_flat_if_needed(6))
                
        # add a major 7 for all chord bases that dont imply a dominant 7
        elif len(schema) < 4:
            schema.append("7")
            
        return schema + self.modifiers
    
        
    
    def get_notes(self):
        if not self.schema:
            self.schema = self.build_schema()
            
        key_ionian = self.key.get_ionian()
        notes = []
        for position in self.schema:
            shift = 0
            for i, character in enumerate(position):
                if character == "b":
                    shift -= 1
                elif character == "#":
                    shift += 1
                else:
                    note = key_ionian[((int(position[i:]) - 1) % 7)]
                    if shift != 0:
                        base_note_index = ALLNOTES.index(note)
                        note = ALLNOTES[base_note_index + shift]
                    notes.append(note)
                    break
        return notes
    
    def to_string(self):
        piano = ASCII_PIANO
        previous_index = 0
        octave = 0
        indexes = []
        for i in self.notes:
            index = ALLNOTES.index(i)
            if index < previous_index:
                octave += 1 
            indexes.append(octave * len(ALLNOTES) + index)
            previous_index = index

        filled_piano = ""
        for line_index, line in enumerate(piano):
            if line_index == 0:
                filled_piano += line + "\n"
                continue
            line = list(line)
            only_whites = line_index > 4
            key_count = 0
            i = 0
            while i < len(line):
                if i == 0 or i == len(line) - 1: 
                    i += 1
                    continue
                
                if (ASCII_WHITES[key_count] if only_whites else key_count) in indexes:
                    while line[i] != "|":
                        line[i] = WHITE_FILL if key_count in ASCII_WHITES or only_whites else BLACK_FILL   
                        i += 1
                
                if line[i] == "|":
                    key_count += 1
                i += 1
            
            filled_piano += "".join(line) + "\n"
        return filled_piano
        

            
   