from collections import Counter
from typing import Dict, TypeVar, Iterable, Generic

T = TypeVar("T")

class SequenceStatistics(Generic[T]):
    """
    Stateless utility for analyzing sequences.

    Provides common frequency analysis without mutating or depending on any specific sequence type.
    Accepts any iterable (e.g. list, tuple, SequenceManipulator, etc.).
    
    This keeps statistics isolated from manipulation logic and makes it reusable in any context 
    (ciphers, engines, data analysis, etc.).

    Examples:
        stats = SequenceStatistics(['A', 'B', 'A', 'C'])
        stats.count_elements()  # {'A': 2, 'B': 1, 'C': 1}
    """

    def __init__(self, sequence: Iterable[T]):
        """
        Initialize the statistics tool with a sequence.

        Args:
            sequence (Iterable[T]): Any sequence-like object.
        """
        self._sequence = sequence

    def count_elements(self) -> Dict[T, int]:
        """
        Return a frequency count of all elements in the sequence.

        Returns:
            Dict[T, int]: A dictionary mapping each unique element to its frequency.
        """
        return dict(Counter(self._sequence))

    def sorted_frequency(self) -> Dict[T, int]:
        """
        Return elements sorted by frequency (descending).

        Returns:
            Dict[T, int]: A dictionary with elements sorted by count descending.
        """
        return dict(Counter(self._sequence).most_common())

