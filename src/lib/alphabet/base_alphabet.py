from dataclasses import dataclass
from typing import List, Tuple

from lib.sequences.sequence import Sequence


@dataclass(frozen=True)
class Alphabet:
    """
    Semantic wrapper for a named character set with associated sequence logic.

    Provides a type-safe, immutable structure for representing alphabets
    based on Unicode ranges, manual definitions, or config files.

    Example:
        >>> a = Alphabet.from_unicode_ranges("basic_latin", [(65, 90)])
        >>> a.name
        'basic_latin'
        >>> a.sequence.data[:3]
        ['A', 'B', 'C']
    """
    name: str
    sequence: Sequence[str]


    @classmethod
    def from_unicode_ranges(cls, name: str, ranges: List[Tuple[int, int]], extras: List[int] = []) -> 'Alphabet':
        chars = [
            chr(code)
            for start, end in ranges
            for code in range(start, end + 1)
        ] + [chr(code) for code in extras]
        sequence = Sequence(chars)
        sequence.validate_unique()
        return cls(name=name, sequence=sequence)

