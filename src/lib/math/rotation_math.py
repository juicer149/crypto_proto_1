from typing import Dict
from math import gcd

def normalize_shift(shift: int, length: int) -> int:
    """
    Normalize a shift value to wrap within a sequence of given length.

    Ensures the shift is correctly bounded to the sequence's index space,
    supporting both positive and negative values.

    Example:
        >>> normalize_shift(4, 3)
        1
        >>> normalize_shift(-1, 3)
        -1
    """
    if length <= 0:
        raise ValueError("Length must be positive.")
    return shift % length if shift >= 0 else -(abs(shift) % length)


def unique_rotation(length: int, step: int) -> int:
    """
    Compute the number of unique rotation positions for a given step and sequence length.

    Equivalent to length // gcd(step, length)

    Example:
        >>> unique_rotation(10, 3)
        10
        >>> unique_rotation(10, 2)
        5
    """
    if length <= 0:
        raise ValueError("Length must be positive.")
    if step == 0:
        raise ValueError("Step must be non-zero.")
    return length // gcd(abs(step), length)


def valid_rotations(length: int) -> Dict[int, int]:
    """
    Generate a dictionary mapping each valid step (1 to length-1)
    to its corresponding unique rotation count.

    Example:
        >>> valid_rotations(6)
        {1: 6, 5: 6, 2: 3, 4: 3, 3: 2}
    """
    if length <= 0:
        raise ValueError("Length must be positive.")
    return {step: unique_rotation(length, step) for step in range(1, length)}

