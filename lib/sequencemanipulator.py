from typing import List, TypeVar, Type, Generic, Iterator, Callable, Tuple


T = TypeVar("T")


class SequenceManipulator(Generic[T]):
    """
    A minimal, strict, fully immutable sequence manipulation tool for generic,
    type-checked sequence operations across different domains.

    Example:
        >>> seq = SequenceManipulator(['A', 'B', 'C'])
        >>> seq2 = seq.rotate_by(1)
        >>> list(seq2)
        ['B', 'C', 'A']

        >>> seq3 = seq2.append('D')
        >>> list(seq3)
        ['B', 'C', 'A', 'D']

        # Original remains unchanged
        >>> list(seq)
        ['A', 'B', 'C']

    This class enforces fail-fast validation on construction, and ensures that
    all operations create new instances. It never mutates internal state.
    """


    def __init__(self, data: List[T], strict: bool = True, expected_type: Type[T] = str):
        """
        Initialize the immutable sequence manipulator.

        Args:
            data (List[T]): The initial sequence.
            strict (bool): Enforce type-checking (default True).
            expected_type (Type[T]): Expected type of all elements (default str).

        Raises:
            TypeError: If strict is True and elements do not match expected_type.
        """
        if strict:
            for i, item in enumerate(data):
                if not isinstance(item, expected_type):
                    raise TypeError(
                        f"Element at index {i} ({item!r}) is not of type {expected_type.__name__}"
                    )
        self._data: Tuple[T, ...] = tuple(data)
        self._strict = strict
        self._expected_type = expected_type


    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self._data)


    def __getitem__(self, index: int) -> T:
        """Return the element at the given index."""
        return self._data[index]


    def __iter__(self) -> Iterator[T]:
        """Iterate over the elements."""
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
        """
        if self._strict:
            for i, item in enumerate(elements):
                if not isinstance(item, self._expected_type):
                    raise TypeError(
                        f"Element at position {i} in extend is not of type {self._expected_type.__name__}"
                    )
        return type(self)(list(self._data) + elements, strict=self._strict, expected_type=self._expected_type)


    def rotate_by(self, shift: int) -> 'SequenceManipulator[T]':
        """
        Return a new sequence rotated by 'shift' positions.

        Args:
            shift (int): Positions to rotate (can be negative).

        Returns:
            SequenceManipulator[T]

        Raises:
            ValueError: If sequence is empty.
        """
        if not self._data:
            raise ValueError("Cannot rotate an empty sequence.")
        length = len(self._data)
        shift = shift % length
        rotated = self._data[shift:] + self._data[:shift]
        return type(self)(list(rotated), strict=self._strict, expected_type=self._expected_type)


    def rotate_generator(self, step: int = 1) -> Iterator['SequenceManipulator[T]']:
        """
        Yield successive rotations by multiples of 'step'.

        Args:
            step (int): Increment per rotation (must be > 0).

        Yields:
            SequenceManipulator[T]

        Raises:
            ValueError: If sequence is empty or step <= 0.
        """
        if not self._data:
            raise ValueError("Cannot rotate an empty sequence.")
        if step <= 0:
            raise ValueError("Step must be a positive integer.")
        seen: set[int] = set()
        length = len(self._data)
        current = 0
        while current not in seen:
            seen.add(current)
            yield self.rotate_by(current)
            current = (current + step) % length


    def move_elements_to_front(self, elements: List[T]) -> Iterator['SequenceManipulator[T]']:
        """
        For each element, move its first occurrence to the front and yield result.

        Args:
            elements (List[T]): Elements to move.

        Yields:
            SequenceManipulator[T]

        Raises:
            ValueError: If sequence is empty.
        """
        if not self._data:
            raise ValueError("Cannot manipulate an empty sequence.")
        for element in elements:
            if element in self._data:
                temp = list(self._data)
                temp.remove(element)
                yield type(self)([element] + temp, strict=self._strict, expected_type=self._expected_type)


    def generate_sequences(self, n: int, generator_func: Callable[[int], List[T]]) -> List['SequenceManipulator[T]']:
        """
        Generate a list of sequences by applying 'generator_func' for each i in range(n).

        Args:
            n (int): Number of sequences.
            generator_func (Callable[[int], List[T]]): Function producing sequence for each i.

        Returns:
            List[SequenceManipulator[T]]

        Raises:
            ValueError: If n <= 0 or n == 1.
        """
        if n <= 0:
            raise ValueError("Cannot generate zero or negative number of sequences.")
        if n == 1:
            raise ValueError("Generating only one sequence is discouraged; use the manipulator directly instead.")
        return [
            type(self)(generator_func(i), strict=self._strict, expected_type=self._expected_type)
            for i in range(n)
        ]

