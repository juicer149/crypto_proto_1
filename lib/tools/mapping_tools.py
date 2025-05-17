# mapping_tools.py

from typing import Dict, Tuple, TypeVar, Generic

T = TypeVar("T")

class MappingMixin(Generic[T]):
    """
    A callable, domain-neutral mapping tool.

    Provides strict, position-by-position mapping between sequences.

    Usage:
        - Called with two sequences:
            Creates a 1:1 substitution map.
            Example: {'A': 'X', 'B': 'Y', 'C': 'Z'}

        - Called with more than two sequences:
            Creates a map where the first sequence is keys,
            and remaining sequences are combined into tuples as values.
            Example: {'A': ('X', 1), 'B': ('Y', 2)}

    Rules:
        - All sequences must have the same length.
        - Fails fast if sequences are of unequal length or less than two.

    Philosophy:
        - Keeps mapping logic separate from sequence manipulation.
        - Stateless and reusable across domains.
        - Intended for engines, pipelines, analyzers, etc.
    """

    def __call__(self, *sequences) -> Dict[T, T] | Dict[T, Tuple[T, ...]]:
        if len(sequences) < 2:
            raise ValueError("At least two sequences are required to build a mapping.")

        reference = sequences[0]
        others = sequences[1:]

        # Fail-fast length validation
        for seq in others:
            if len(seq) != len(reference):
                raise ValueError(f"All sequences must be of equal length ({len(reference)} vs {len(seq)}).")

        if len(others) == 1:
            return dict(zip(reference, others[0]))
        else:
            return {
                reference[i]: tuple(seq[i] for seq in others)
                for i in range(len(reference))
            }


"""
future feature
def invert_mapping(mapping: Dict[T, T]) -> Dict[T, T]:
    """
    # Invert a simple 1:1 mapping.
    """
    return {v: k for k, v in mapping.items()}
"""
