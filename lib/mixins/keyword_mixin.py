# tools/keyword_mixin.py

from tools.sequencemanipulator import SequenceManipulator

class KeywordMixin:
    """
    Mixin that provides keyword‐based sequence manipulation.

    When called with a keyword string:
      1. Removes duplicate characters from the keyword, preserving first occurrences.
      2. Reverses the order of the unique keyword characters.
      3. For each character in that reversed list, moves its first occurrence in
         the sequence to the front, using SequenceManipulator.move_elements_to_front().

    Returns:
        SequenceManipulator[str]: The fully transformed sequence.

    Usage:
        class SomeEngine(KeywordMixin):
            def __init__(self, sequence: SequenceManipulator[str]):
                self.sequence = sequence

        engine = SomeEngine(seq)
        result = engine("SECRET")  # SequenceManipulator with keyword applied
    """

    def __call__(self, keyword: str) -> SequenceManipulator[str]:
        if not hasattr(self, 'sequence'):
            raise AttributeError(
                "KeywordMixin requires 'self.sequence' to be set to a SequenceManipulator instance before calling."
            )
        if len(self.sequence) == 0:
            raise ValueError("Cannot manipulate an empty sequence in KeywordMixin.")

        # Deduplicate keyword (preserve first occurrence)
        seen: set[str] = set()
        dedup_list: list[str] = [
            c for c in keyword if not (c in seen or seen.add(c))
        ]

        # Move each deduplicated character, in reverse order, to front
        seq: SequenceManipulator[str] = self.sequence
        for char in reversed(dedup_list):
            gen = seq.move_elements_to_front([char])
            seq = next(gen)

        return seq
