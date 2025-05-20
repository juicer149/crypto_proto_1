from typing import Callable, Iterable, Iterator, List, TypeVar
import warnings

from lib.math.rotation_math import normalize_shift, unique_rotation


T = TypeVar("T")


class SequenceTool:
    """
    Stateless utility class for performing various sequence transformations.

    Example:
        >>> SequenceTool.rotate(['A', 'B', 'C'], 1)
        ['C', 'A', 'B']
    """

    @staticmethod
    def rotate(seq: List[T], shift: int) -> List[T]:
        """
        Rotate a sequence by a given shift.

        Example:
            >>> SequenceTool.rotate(['A', 'B', 'C'], -1)
            ['B', 'C', 'A']
        """
        if not seq:
            raise ValueError("Cannot rotate an empty sequence.")
        length = len(seq)
        normalized_shift = normalize_shift(shift, length)
        return seq[-normalized_shift:] + seq[:-normalized_shift] if normalized_shift else list(seq)


    @staticmethod
    def rotate_generator(seq: List[T], step: int = 1) -> Iterator[List[T]]:
        """
        Generate all distinct rotations by a given step.

        Example:
            >>> gen = SequenceTool.rotate_generator(['A', 'B', 'C'], 1)
            >>> [next(gen) for _ in range(3)]
            [['A', 'B', 'C'], ['C', 'A', 'B'], ['B', 'C', 'A']]
        """
        if not seq:
            raise ValueError("Cannot rotate an empty sequence.")
        if step == 0:
            raise ValueError("Step must be non-zero.")

        length = len(seq)
        norm_step = normalize_shift(step, length)

        expected = unique_rotation(length, norm_step)

        seen = set()
        current = 0
        while current not in seen:
            seen.add(current)
            yield SequenceTool.rotate(seq, current)
            current = (current + norm_step) % length

        if len(seen) != expected:
            warnings.warn("Generated fewer unique rotations than expected.")


    @staticmethod
    def from_generator(n: int, generator_func: Callable[[int], List[T]], mode: str = 'default') -> List[List[T]]:
        """
        Generate sequences using a custom generator function.

        Example:
            >>> def gen(i): return [chr(65 + (j + i) % 3) for j in range(3)]
            >>> SequenceTool.from_generator(3, gen)
            [['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']]
        """
        if n <= 0:
            raise ValueError("Cannot generate zero or negative number of sequences.")
        if n == 1:
            raise ValueError("Generating only one sequence is discouraged.")

        result = [generator_func(i) for i in range(n)]
        if mode == 'mirror':
            return [list(reversed(seq)) for seq in result]
        return result


    @staticmethod
    def move_elements_to_front(seq: List[T], elements: List[T]) -> Iterator[List[T]]:
        """
        Yield new sequences with specified elements moved to front.

        Example:
            >>> list(SequenceTool.move_elements_to_front(['A', 'B', 'C'], ['C']))
            [['C', 'A', 'B']]
        """
        if not seq:
            raise ValueError("Cannot manipulate an empty sequence.")
        for element in elements:
            if element in seq:
                temp = list(seq)
                temp.remove(element)
                yield [element] + temp


    @staticmethod
    def index_of(seq: List[T], value: T) -> int:
        """
        Get index of a value in a sequence.

        Example:
            >>> SequenceTool.index_of(['A', 'B', 'C'], 'B')
            1
        """
        return seq.index(value)

