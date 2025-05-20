from typing import List, TypeVar, Generic, Iterator
from dataclasses import dataclass


from .sequence_tool import SequenceTool  # lokal import
from ..math.rotation_math import normalize_shift  # relativ import


T = TypeVar("T")


@dataclass(frozen=True)
class Sequence(Generic[T]):
    """
    Immutable sequence wrapper with transformation support.

    Example:
        >>> s = Sequence(['A', 'B', 'C'])
        >>> s.rotate(1).data
        ['C', 'A', 'B']
    """
    data: List[T]


    def rotate(self, shift: int) -> 'Sequence[T]':
        return Sequence(SequenceTool.rotate(self.data, shift))


    def index_of(self, value: T) -> int:
        return self.data.index(value)


    def move_to_front(self, elements: List[T]) -> Iterator['Sequence[T]']:
        for variant in SequenceTool.move_elements_to_front(self.data, elements):
            yield Sequence(variant)


    def validate_unique(self) -> None:
        if len(set(self.data)) != len(self.data):
            raise ValueError("Sequence contains duplicate values.")


    def __len__(self):
        return len(self.data)


    def __iter__(self):
        return iter(self.data)


    def __getitem__(self, index):
        return self.data[index]

