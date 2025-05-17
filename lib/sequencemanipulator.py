# sequencemanipulator.pyfrom typing import List, TypeVar, Type, Generic, Iterator, Dict, Callable

T = TypeVar("T")

class SequenceManipulator(Generic[T]):
    """
    A minimal, strict sequence manipulation tool designed for reusability
    across different domains such as ciphers, engines, and data analysis.

    This class focuses solely on generic, type-checked sequence operations 
    and enforces fail-fast validation on both construction and mutations. 
    
    The manipulator does not impose any domain-specific semantics like "alphabet"
    or "ROT". Such logic should be composed in higher layers or engines 
    using this tool as a foundation.

    The manipulator is immutable in 'push' operations (producing new views),
    but allows controlled mutation via 'append' and 'extend' when explicitly chosen.
    """

    def __init__(self, data: List[T], strict: bool = True, expected_type: Type[T] = str):
        """
        Initialize the sequence manipulator.

        Args:
            data (List[T]): The initial sequence.
            strict (bool): If True (default), enforce that all elements are of 'expected_type'.
            expected_type (Type[T]): The expected type of all elements (default: str).

        Raises:
            TypeError: If 'strict' is True and elements do not match 'expected_type'.
        """
        if strict:
            for i, item in enumerate(data):
                if not isinstance(item, expected_type):
                    raise TypeError(
                        f"Element at index {i} ({item!r}) is not of type {expected_type.__name__}"
                    )
        self._data = data
        self._strict = strict
        self._expected_type = expected_type


    def __len__(self) -> int:
        return len(self._data)


    def __getitem__(self, index: int) -> T:
        return self._data[index]


    def __iter__(self) -> Iterator[T]:
        return iter(self._data)


    def __add__(self, other: 'SequenceManipulator[T]') -> Dict[T, T]:
        """
        Create a substitution map by pairing this sequence with another.
        """
        if len(self) != len(other):
            raise ValueError(
                f"Cannot build substitution map: lengths differ ({len(self)} vs {len(other)})"
            )
        return dict(zip(self._data, other._data))


    def append(self, element: T) -> None:
        """
        Append an element to the sequence.

        In strict mode, the type of the element will be validated.

        Args:
            element (T): The element to append.

        Raises:
            TypeError: If strict and type mismatch.
        """
        # Funderade här kring om man skulle skriv om denna till __add__
        # så listan + element appendar, men skulle du även vilja skapa logik 
        # för om man försöker + ihop två listor 
        if self._strict and not isinstance(element, self._expected_type):
            raise TypeError(
                f"Element {element!r} is not of type {self._expected_type.__name__}"
            )
        self._data.append(element)


    def extend(self, elements: List[T]) -> None:
        """
        Extend the sequence with a list of elements.

        In strict mode, all elements will be validated.

        Args:
            elements (List[T]): The elements to add.

        Raises:
            TypeError: If strict and any element is of wrong type.
        """

        if self._strict:
            for i, item in enumerate(elements):
                if not isinstance(item, self._expected_type):
                    raise TypeError(
                        f"Element at position {i} in extend is not of type {self._expected_type.__name__}"
                    )
        self._data.extend(elements)


    def rotate_by(self, shift: int) -> 'SequenceManipulator[T]':
        """
        Return a new SequenceManipulator with elements rotated by `shift` positions.

        Positive `shift` moves elements from front toward end.
        Negative `shift` moves elements from end toward front.

        Examples:
            seq = SequenceManipulator(['A','B','C','D'])
            seq.rotate_by(1)   # SequenceManipulator(['B','C','D','A'])
            seq.rotate_by(-1)  # SequenceManipulator(['D','A','B','C'])

        Args:
            shift (int): Number of positions to rotate. Can be negative.

        Returns:
            SequenceManipulator[T]: A new instance with rotated data.

        Raises:
            ValueError: If the sequence is empty.
        """
        if not self._data:
            raise ValueError("Cannot rotate an empty sequence.")

        length = len(self._data)
        # normalize shift to positive within range [0, length)
        shift = shift % length
        rotated = self._data[shift:] + self._data[:shift]
        return SequenceManipulator(rotated, strict=self._strict, expected_type=self._expected_type)


    def rotate_generator(self, step: int = 1) -> Iterator['SequenceManipulator[T]']:
        """
        Yield successive rotations of the sequence by multiples of `step`,
        until the full cycle is completed (returns to the original order).

        Examples:
            seq = SequenceManipulator(['A','B','C'])
            for s in seq.rotate_generator(1):
                print(s)
            # yields: ['A','B','C'], ['B','C','A'], ['C','A','B']

        Args:
            step (int): The increment of positions to rotate for each iteration.
                        Must be a positive integer.

        Yields:
            SequenceManipulator[T]: Next rotated sequence in the cycle.

        Raises:
            ValueError: If the sequence is empty or `step` is not positive.
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
        For each element in the list, move its first occurrence to the front, yield result.
        Does not check for duplicates in 'elements' itself.
        
        Fails fast if sequence is empty.
        """
        if not self._data:
            raise ValueError("Cannot manipulate an empty sequence.")

        for element in elements:
            if element in self._data:
                seq = self._data[:]
                seq.remove(element)
                yield SequenceManipulator([element] + seq, strict=self._strict, expected_type=self._expected_type)


    def generate_sequences(self, n: int, generator_func: Callable[[int], List[T]]) -> List['SequenceManipulator[T]']:
        """
        Generate a list of SequenceManipulator instances by applying 'generator_func'
        for i in range(n).

        This method is intentionally agnostic to any domain logic (e.g. ROT, keyword, Vigenère).
        It simply applies the provided 'generator_func' with the current index and expects
        a list of elements in return, which will be wrapped in a new SequenceManipulator.

        Use case example (in a cipher engine):
            - Create a sequence of alphabets for Vigenère, where each is shifted by the key.
            - Create dynamic alphabets using a keyword or Alberti logic.
        
        The engine or caller is fully responsible for providing the correct logic;
        this method only handles the wrapping and iteration.

        Fails fast:
            - If n <= 0: Raises ValueError.
            - If n == 1: Raises ValueError suggesting to use manipulator directly instead.

        Args:
            n (int): Number of sequences to generate.
            generator_func (Callable[[int], List[T]]): Function taking an index and returning a list.

        Returns:
            List[SequenceManipulator[T]]: Generated sequence manipulators.
        """
        if n <= 0:
            raise ValueError("Cannot generate zero or negative number of sequences.")
        if n == 1:
            raise ValueError("Generating only one sequence is discouraged; use the manipulator directly instead.")

        return [
            type(self)(generator_func(i), strict=self._strict, expected_type=self._expected_type)
            for i in range(n)
        ]
