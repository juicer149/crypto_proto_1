from typing import List

from lib.dataclasses import Alphabet


class VigenereTable:
    """
    Represents a full polyalphabetic table based on a base alphabet.

    Internally stores a list of rotated Alphabets (one per ROT).
    Used for polyalphabetic substitution systems like Vigenère.
    """


    def __init__(self, base_alphabet: Alphabet):
        self.base = base_alphabet
        self.rows: List[Alphabet] = [
            Alphabet(name=f"ROT{i}", sequence=seq)
            for i, seq in enumerate(base_alphabet.sequence.rotate_generator(1))
        ]


    def __getitem__(self, index: int) -> Alphabet:
        """
        Access a rotated Alphabet by index (0 = unshifted).
        """
        return self.rows[index % len(self.rows)]


    def lookup(self, plain: str, key: str) -> str:
        """
        Get the cipher character for a given plain/key pair.

        Looks up the column for plain in the row given by key.
        """
        row_index = self.base.sequence.index_of(key)
        col_index = self.base.sequence.index_of(plain)
        return self[row_index].sequence[col_index]


