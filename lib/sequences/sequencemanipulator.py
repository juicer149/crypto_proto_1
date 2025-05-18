"""
SequenceManipulator
--------------------
A generic, immutable sequence transformation utility.

Supports rotation, mapping, keyword manipulation, and indexed generation. 
Designed for cryptographic use, but applicable across any domain
where immutable list transformations are needed.

Examples:
    >>> from sequencemanipulator import SequenceManipulator
    >>> seq = SequenceManipulator(['A', 'B', 'C'])
    >>> list(seq.rotate_by(1))
    ['C', 'A', 'B']
"""


from typing import Callable, Generic, Iterable, Iterator, List, Tuple, TypeVar, Type
from math import gcd
import warnings


T = TypeVar("T")


class SequenceManipulator(Generic[T]):
    """
    A minimal, strict, fully immutable sequence manipulation tool for generic,
    type-checked operations across different domains.

    Typical use cases:
        - Constructing cipher alphabets (e.g. ROT, Vigenère)
        - Rotating or reshaping base sequences
        - Generating transformations through indexed logic

    This class is designed to be composable and predictable:
        - `rotate_by` handles basic Caesar/ROT transformations.
        - `rotate_generator` automates successive rotations (e.g. for full-cycle steps).
        - `generate_sequences` supports fully custom logic per step/index, enabling
      dynamic or keyword-based transformations.

    This class enforces fail-fast validation on construction, and ensures that
    all operations create new instances. It never mutates internal state.


    Example:
        >>> seq = SequenceManipulator(['A', 'B', 'C'])
        >>> rotated = seq.rotate_by(1)
        >>> updated = rotated.append('D')
        >>> list(updated)
        ['C', 'A', 'B', 'D']
    """

    __slots__ = ('_data', '_strict', '_expected_type')


    def __init__(self, data: List[T], strict: bool = True, expected_type: Type[T] = str):
        """
        Initialize the immutable sequence manipulator.

        Args:
            data (List[T]): The initial sequence.
            strict (bool): Enforce type-checking (default True).
            expected_type (Type[T]): Expected type of all elements (default str).

        Raises:
            TypeError: If strict is True and elements do not match expected_type.
        
        Example:
            >>> list(SequenceManipulator(['A', 'B']))
            ['A', 'B']

            >>> SequenceManipulator(['A', 1])   # doctest: +ELLIPSIS
            Traceback (most recent call last):
            TypeError: ...
        """

        self._data: Tuple[T, ...] = tuple(data)
        self._strict = strict
        self._expected_type = expected_type

        if self._strict:
            invalid_items = [
                    (i, item) for i, item in enumerate(data) 
                    if not isinstance(item, self._expected_type)]
            if invalid_items:
                details = ", ".join(f"index {i}: {item!r}" for i, item in invalid_items)
                raise TypeError(f"Elements with invalid types found: {details}")



    def __repr__(self) -> str:
        """
        Represent the sequence cleanly for REPL/debugging.
        
        Example:
            >>> SequenceManipulator(['X', 'Y'])
            SequenceManipulator(['X', 'Y'])
        """
        return f"{self.__class__.__name__}({list(self._data)})"


    @classmethod
    def with_type(
            cls: Type['SequenceManipulator[T]'], 
            data: Iterable[T], 
            expected_type: Type[T]
            ) -> 'SequenceManipulator[T]':
        """
        Factory class to clearly specify expected type.
        This makes the API more explicit and shifts type declaration to construction time.

        Example:
            >>> SequenceManipulator.with_type(['X', 'Y'], str)
            SequenceManipulator(['X', 'Y'])
        """
        return cls(data, strict=True, expected_type=expected_type)

    def __len__(self) -> int:
        """
        Return the number of elements.
        
        Example:
            >>> seq = SequenceManipulator(['A', 'B', 'C',])
            >>> len(seq)
            3
        """

        return len(self._data)


    def __getitem__(self, index: int) -> T:
        """
        Return the element at the given index.
        
        Example:
            >>> SequenceManipulator(['A', 'B', 'C'])[0]
            'A'
            >>> SequenceManipulator(['A', 'B', 'C'])[-1]
            'C'
        """

        return self._data[index]


    def __iter__(self) -> Iterator[T]:
        """
        Iterate over the elements.

        Example:
            >>> list(SequenceManipulator(['A', 'B', 'C']))
            ['A', 'B', 'C']
        """

        return iter(self._data)


    def append(self, element: T) -> 'SequenceManipulator[T]':
        """
        Return a new sequence with 'element' appended.

        Args:
            element (T): The element to append.

        Returns:
            SequenceManipulator[T]

        Raises:
            TypeError: If strict and type mismatch.

        Example:
            >>> list(SequenceManipulator(['A', 'B']).append('C'))
            ['A', 'B', 'C']
            >>> SequenceManipulator(['A']).append(1)    # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            TypeError: ... 
        """

        if self._strict and not isinstance(element, self._expected_type):
            raise TypeError(
                f"Element {element!r} is not of type {self._expected_type.__name__}"
            )
        return type(self)(list(self._data) + [element], strict=self._strict, expected_type=self._expected_type)


    def extend(self, elements: List[T]) -> 'SequenceManipulator[T]':
        """
        Return a new sequence with 'elements' appended.

        Args:
            elements (List[T]): Elements to append.

        Returns:
            SequenceManipulator[T]

        Raises:
            TypeError: If strict and any element has wrong type.

        Example:
            >>> list(SequenceManipulator(['A']).extend(['B', 'C']))
            ['A', 'B', 'C']
            >>> SequenceManipulator(['A']).extend(['B', 1])  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            TypeError: ...
        """

        elements = list(elements)

        if self._strict:
            for i, item in enumerate(elements):
                if not isinstance(item, self._expected_type):
                    raise TypeError(
                        f"Element at position {i} in extend is not of type {self._expected_type.__name__}"
                    )
        return type(self)(list(self._data) + elements, strict=self._strict, expected_type=self._expected_type)


    def rotate_by(self, shift: int) -> 'SequenceManipulator[T]':
        """
        Create a rotated copy of the sequence.

        Useful for Caesar/ROT-style operations or offset-based transformations.

        Args:
            shift (int): Positions to rotate (can be negative).
                         Positive = right shift, negative = left shift.

        Returns:
            SequenceManipulator[T]

        Raises:
            ValueError: If sequence is empty.

        Example:
            >>> list(SequenceManipulator(['A', 'B', 'C']).rotate_by(-1))
            ['B', 'C', 'A']
            >>> list(SequenceManipulator(['A', 'B', 'C']).rotate_by(4))
            ['C', 'A', 'B']
            >>> SequenceManipulator([]).rotate_by(1)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ValueError: ...
        """

        if not self._data:
            raise ValueError("Cannot rotate an empty sequence.")

        data = self._data
        length = len(data)
        normalized_shift = shift % length if shift >= 0 else -(abs(shift) % length)

        if normalized_shift == 0:
            rotated = data
        else:
            rotated = data[-normalized_shift:] + data[:-normalized_shift]

        return type(self)(list(rotated), strict=self._strict, expected_type=self._expected_type)



    def rotate_generator(self, step: int = 1) -> Iterator['SequenceManipulator[T]']:
        """
        Yield successive rotations by multiples of 'step'.

        Args:
            step (int): Increment per rotation (must be > 0).

        Yields:
            SequenceManipulator[T]: Rotades sequences.

        Raises:
            ValueError: If sequence is empty or step <= 0.

        Cipher use case:
            Useful for generating a full set of rotated alphabets (e.g. for
            polyalphabetic ciphers). A step of 1 yields a full rotation cycle.
            Steps like 3 or 7 can produce more irregular, but still complete
            permutations for use in alternative cipher schemes.

        Example:
            >>> gen = SequenceManipulator(['A', 'B', 'C']).rotate_generator(1)
            >>> [list(next(gen)) for _ in range(3)]
            [['A', 'B', 'C'], ['C', 'A', 'B'], ['B', 'C', 'A']]
            
        """
        if not self._data:
            raise ValueError("Cannot rotate an empty sequence.")
        if step <= 0:
            raise ValueError("Step must be a positive integer.")

        if gcd(step, len(self._data)) != 1:
            warnings.warn(
                f"rotate_generator: step {step} is not coprime with length {len(self._data)}. Full cycle not guaranteed."
            ) # lägg till denna i doctest

        seen: set[int] = set()
        length = len(self._data)
        current = 0
        while current not in seen:
            seen.add(current)
            yield self.rotate_by(current)
            current = (current + step) % length

    def cycle_length(self, step: int) -> int:
        """
        Returns number of unique rotations based on step.
        
        Example:
            >>> SequenceManipulator(['A', 'B', 'C']).cycle_length(1)
            3
        """
        return len(self._data) // gcd(step, len(self._data))


    def from_generator(
            self, n: int, 
            generator_func: Callable[[int], 
            Iterator[T]]
            ) -> List['SequenceManipulator[T]']:
        """
        Generate a list of sequences by applying 'generator_func' for each i in range(n).

        Args:
            n (int): Number of sequences.
            generator_func (Callable[[int], List[T]]): Function producing sequence for each i.

        Returns:
            List[SequenceManipulator[T]]

        Raises:
            ValueError: If n <= 0 or n == 1.

        Cipher use case:
            Offers full flexibility for cipher-specific logic such as:
                - Keyword-based shifting
                - Alberti-style dynamic alphabets
                - Custom index-dependent mappings

            While `rotate_generator` provides standard cyclic shifting,
            this method is intended for arbitrary generation, not limited
            to rotation.

        Example:
            >>> def gen(i): return [chr(65 + (j + i) % 3) for j in range(3)]
            >>> seqs = SequenceManipulator(['A', 'B', 'C']).from_generator(3, gen)
            >>> [list(seq) for seq in seqs]
            [['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']]
        """

        if n <= 0:
            raise ValueError("Cannot generate zero or negative number of sequences.")

        if n == 1:
            raise ValueError("Generating only one sequence is discouraged; use the manipulator directly instead.")

        return [
            type(self)(generator_func(i), strict=self._strict, expected_type=self._expected_type)
            for i in range(n)
        ]


    def move_elements_to_front(self, elements: List[T]) -> Iterator['SequenceManipulator[T]']:
        """
        For each element, move its first occurrence to the front and yield result.

        Args:
            elements (List[T]): Elements to move.

        Yields:
            SequenceManipulator[T]

        Raises:
            ValueError: If sequence is empty.

        Example:
            >>> seq = SequenceManipulator(['A', 'B', 'C'])
            >>> list(next(seq.move_elements_to_front(['C'])))
            ['C', 'A', 'B']
        """

        if not self._data:
            raise ValueError("Cannot manipulate an empty sequence.")
        for element in elements:
            if element in self._data:
                temp = list(self._data)
                temp.remove(element)
                yield type(self)([element] + temp, strict=self._strict, expected_type=self._expected_type)
