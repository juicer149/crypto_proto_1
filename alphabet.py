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
)

from load_yaml import load_yaml

T = TypeVar("T", bound=str)


class Alphabet(Generic[T]):
    """
    A composable Alphabet class for substitution ciphers.

    Features:
      - Load definitions from a YAML (ranges + extras).
      - Caesar rotations via `alphabet * shift` or `shift * alphabet`.
      - Build substitution maps between two Alphabets of equal length.
      - Iterate through successive rotations with `.rotations(step)`.
    """

    def __init__(self, chars: List[T]) -> None:
        if not chars:
            raise ValueError("Alphabet cannot be empty")
        self._chars: List[T] = chars

    def __len__(self) -> int:
        return len(self._chars)

    def __getitem__(self, index: int) -> T:
        return self._chars[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self._chars)

    @classmethod
    def from_config(
        cls,
        language: str,
        config_path: str = "config/charsets.yaml"
    ) -> "Alphabet[T]":
        """
        Load an alphabet for `language` from YAML at `config_path`.

        Raises:
            ValueError if `language` is not defined in the file.
        """
        data: Dict[str, Any] = load_yaml(config_path)
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
        # Add extras
        chars += [chr(code) for code in cfg.get("extras", [])]

        return cls(chars)

    def __mul__(self, shift: int) -> "Alphabet[T]":
        """
        Return a new Alphabet rotated by `shift` positions.

        Args:
            shift: positions to rotate by.

        Returns:
            Alphabet[T]
        """
        length = len(self)
        offset = shift % length
        rotated_chars = self._chars[offset:] + self._chars[:offset]
        return type(self)(rotated_chars)

    __rmul__ = __mul__

    def substitution_map(self, other: "Alphabet[T]") -> Dict[T, T]:
        """
        Map this alphabet to `other`, position by position.

        Raises:
            ValueError if lengths differ.
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

        Example:
            for alpha in alphabet.rotations(5):
                print(alpha)
        """
        seen = set()
        current = 0
        length = len(self)

        while current not in seen:
            seen.add(current)
            yield self * current
            current = (current + step) % length

