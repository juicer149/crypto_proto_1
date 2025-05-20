from typing import List, Dict
from lib.alphabet.base_alphabet import Alphabet
from lib.sequences.sequence import Sequence


class RotationTable:
    """
    Rotation-based substitution table (optimized).

    Stores rotation rows as lists only, and uses base sequence for lookup.
    More memory-efficient than mapping-based versions.

    Example:
        >>> base = Alphabet.from_unicode_ranges("latin", [(65, 90)])
        >>> table = RotationTable(base, step=1)
        >>> table.lookup('A', 'B')  # ROT 1
        'B'
    """


    def __init__(self, base_alphabet: Alphabet, step: int = 1):
        self.base = base_alphabet
        self.step = step
        self.rows: Dict[int, List[str]] = {
            i: row for i, row in enumerate(self.base.sequence.rotate_generator(step))
        }


    def __getitem__(self, index: int) -> List[str]:
        return self.rows[index % len(self.rows)]


    def lookup(self, plain: str, key: str) -> str:
        """
        Get the cipher character for a given plain/key pair using index-based lookup.
        """
        row_index = self.base.sequence.index_of(key)
        col_index = self.base.sequence.index_of(plain)
        return self[row_index][col_index]

