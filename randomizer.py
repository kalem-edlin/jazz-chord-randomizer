import datetime as d
import os
import random

import structure as s


def main():
    
    file_path = "./chords.txt" 
    chords = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip() 
            chords.append(line)
    
    while(True):
        chord_txt = random.choice(chords)
        root = random.choice(s.ALLNOTES)
        try:
            chord = s.Chord(root, chord_txt)
            print(f"{root}{chord_txt}")
            print(chord.schema)
            input("Press enter to unlock Piano View...")
            print(chord.keyboard)
            user_input = input("Press enter for a new chord or type stop: ")
            if user_input == "stop":
                break
            print("\n")
        except Exception as e:
            print("Error occured, please check logs...")

if __name__ == "__main__":
    main()