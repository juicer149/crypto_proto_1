from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Alphabet:
    """
    A thin, immutable semantic adapter representing a specific alphabet
    composed from Unicode ranges, YAML configurations, or manual definitions.

    It internally wraps a SequenceManipulator and exposes domain-specific 
    semantics like substitution_map, while keeping the sequence manipulation 
    generic and reusable.
    """
    name: str
    sequence: SequenceManipulator[str]

    @classmethod
    def from_unicode_ranges(cls, name: str, ranges: List[tuple[int, int]], extras: List[int] = []):
        chars = [
            chr(code)
            for start, end in ranges
            for code in range(start, end + 1)
        ] + [chr(code) for code in extras]
        seq = SequenceManipulator(chars, strict=True)
        return cls(name=name, sequence=seq)

    # kommer nog ta bort denna då den inte tillhör alphabet strict utan mer är en 
    # funktion för att manipulera listor och som kan göras mer abstrakt i 
    def substitution_map(self, other: 'Alphabet') -> dict[str, str]:
        """
        Delegates to the underlying SequenceManipulator to create a substitution map.
        """
        return self.sequence.substitution_map(other.sequence)

    def push(self):
        """
        Delegates to the underlying SequenceManipulator push generator.
        """
        return self.sequence.push()
