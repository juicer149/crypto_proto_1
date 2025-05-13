# rot_engine.py

from alphabet import Alphabet

class RotEngine:
    """
    Core ROT engine that produces substitution maps given a shift and an Alphabet.
    This can be reused by Caesar, ROT13, Vigenère, Alberti, etc.
    """

    def __init__(self, alphabet: Alphabet):
        self.alphabet = alphabet

    def get_substitution_map(self, shift: int) -> dict:
        shifted_alphabet = self.alphabet * shift
        return self.alphabet.substitution_map(shifted_alphabet)
