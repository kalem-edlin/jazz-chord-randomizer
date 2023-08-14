import os
import unittest

import structure as s


class TestCases(unittest.TestCase):
    
    def setUp(self) -> None:
        self.chords = []
        with open("./chords.txt", 'r') as file:
            for line in file:
                line = line.strip() 
                self.chords.append(line)

        return super().setUp()

    def test_all_chord_combinations(self):
        all_passed = True
        for root in s.ALLNOTES:
            for chord_text in self.chords:
                try:
                    s.Chord(root, chord_text)
                except Exception as e:
                    all_passed = False
                    pass
        self.assertTrue(all_passed)
        
    def test_minor_sixth(self):
        chord = s.Chord("C", "-6")
        self.assertEquals(chord.schema, ["1", "b3", "5", "b6"])
        
    def test_minor_major_seventh(self):
        chord = s.Chord("C", "-△7")
        self.assertEquals(chord.schema, ["1", "b3", "5", "7"])
        

if __name__ == '__main__':
    unittest.main()