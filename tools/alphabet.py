# alphabet.py

import yaml
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    TypeVar,
    Generic,
    Iterator,
    Optional
)

from config_loader import load_config

T = TypeVar("T", bound=str)


class Alphabet(Generic[T]):
    """
    A composable Alphabet class for substitution ciphers.

    This class supports loading alphabets from YAML files, performing rotations 
    like Caesar/ROT, and generating substitution mappings.

    Features:
        - Load definitions from a YAML file (ranges + extras).
        - Caesar/ROT rotations via `alphabet * shift`.
        - Build substitution maps between alphabets of equal length.
        - Iterate through successive rotations with `.rotations(step)`.

    Example:
        alpha = Alphabet(['A', 'B', 'C'])
        print(alpha[1])  # Outputs "B"
        for letter in alpha:
            print(letter)

    Tech Dept(TD):
        1: make a config dataclass that holds the value of 'config/charsets.yaml'
            - and to load those configs files to be able to only change in one file
    """


    def __init__(self, chars: List[T]) -> None:
        if not chars:
            raise ValueError("Alphabet cannot be empty")
        self._chars: List[T] = chars


    def __len__(self) -> int:
        return len(self._chars)


    def __getitem__(self, index: int) -> T:
        """
        Get the character at a given index or a sub-Alphabet from a slice.

        If given an integer index, returns the character at that position.
        If given a slice, returns a new Alphabet containing the sliced characters.

        Examples:
            a = Alphabet(['A', 'B', 'C', 'D'])
            a[1]      # 'B'
            a[:2]     # Alphabet(['A', 'B'])

        Args:
            index (int or slice): The position or slice to retrieve.

        Returns:
            str: If index is an integer.
            Alphabet[T]: If index is a slice.
        """
        if isinstance(index, slice):
            return type(self)(self._chars[index])
        else:
            return self._chars[index]


    def __iter__(self) -> Iterator[T]:
        return iter(self._chars) 


    @classmethod
    def from_config(
        cls,
        language: str,
        config_path: str = "config/charsets.yaml",   # TD 1
        user_extras: Optional[List[int]] = None,

    ) -> "Alphabet[T]":
        """
        Load an alphabet for `language` from YAML at `config_path`,
        optionally adding user-specified extra characters.

        Args:
            language (str): Language key in YAML.
            config_path (str): Path to YAML.
            user_extras (Optional[List[int]]): Additional characters (as code points)

        Raises:
            ValueError if `language` is not defined in the file.

        Returns:
            Alphabet[T]

        Example:
            # Load English from YAML and add special symbols
            Alphabet.from_config("en", user_extras=[8364, 163])  # Adds €, £

        """
        data: Dict[str, Any] = load_config(config_path)
        alphabets = data.get("alphabets", {})

        if language not in alphabets:
            raise ValueError(f"Unknown language: {language!r}")

        cfg = alphabets[language]

        # Build from ranges
        chars: List[T] = [
            chr(code)
            for start, end in cfg.get("ranges", [])
            for code in range(start, end + 1)
        ]

        # Combine YAML extras and user_extras
        extras = cfg.get("extras", [])
        if user_extras:
            extras += user_extras

        chars += [chr(code) for code in extras]

        return cls(chars)


    def __mul__(self, shift: int) -> "Alphabet[T]":
        """
        Return a new Alphabet rotated by `shift` positions.

        Args:
            shift: positions to rotate by.

        Returns:
            Alphabet[T]

        Example: 
            - ROT13 = Alphabet * 13
        """
        length = len(self)
        offset = shift % length
        rotated_chars = self._chars[offset:] + self._chars[:offset]
        return type(self)(rotated_chars)

    # Allow both `alphabet * x` and `x * alphabet`
    __rmul__ = __mul__ 


    def substitution_map(self, other: "Alphabet[T]") -> Dict[T, T]:
        """
        Map this alphabet to `other` alphabet, position by position.

        Raises:
            ValueError: If the two alphabets differ in length.

        Example:
            alpha1 = Alphabet(['A', 'B', 'C'])
            alpha2 = Alphabet(['X', 'Y', 'Z'])
            mapping = alpha1.substitution_map(alpha2)
            # {'A': 'X', 'B': 'Y', 'C': 'Z'}
        """
        if len(self) != len(other):
            raise ValueError(
                f"Cannot build substitution map: "
                f"lengths differ ({len(self)} vs {len(other)})"
            )
        return dict(zip(self._chars, other._chars))


    def rotations(self, step: int = 1) -> Iterator["Alphabet[T]"]:
        """
        Yield successive rotations by multiples of `step` until full cycle.

        Args:
            step (int): Rotation step size.

        Example:
            for alpha in alphabet.rotations(5):
                print(alpha)
        """
        length = len(self)
        for i in range(0, length, step):
            yield self * i

