# base_rot_engine.py
from abc import ABC, abstractmethod


class AbstractRotEngine(ABC):
    """
    Abstract ROT engine that produces substitution maps given a shift and an Alphabet.
    This can be reused by Caesar, ROT13, Vigenère, Alberti, etc.
    """

    def __init__(self, alphabet):
        self.alphabet = alphabet

    
    @abstractmethod
    def get_substitution_map(self, pos: int):
        """ Returns substitutionan map depanding on positions in the text"""
        ...


#Skriva kommentarer
class StaticRot(AbstractRotEngine):
    def __init__(self, alphabet, shift):
        super().__init__(alphabet)
        self._map = alphabet.substitution_map(alphabet * shift)

    def get_substitution_for_position(self, pos):
        return self._map


class AlbertiRot(AbstractRotEngine):
    def __init__(self, alphabet, initial_shift, shift_interval, shift_step):
        super().__init__(alphabet)
        self.initial_shift = initial_shift
        self.shift_interval = shift_interval
        self.shift_step = shift_step

    def get_substitution_for_position(self, pos):
        shift_count = (pos // self.shift_interval) * self.shift_step
        total_shift = (self.initial_shift + shift_count) % len(self.alphabet)
        return self.alphabet.substitution_map(self.alphabet * total_shift)


class VigenereRot(AbstractRotEngine):
    def __init__(self, alphabet, key_stream):
        super().__init__(alphabet)
        self.key_stream = [alphabet.index(char) for char in key_stream]

    def get_substitution_for_position(self, pos):
        shift = self.key_stream[pos % len(self.key_stream)]
        return self.alphabet.substitution_map(self.alphabet * shift)
