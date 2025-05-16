# tools/rot_mixin.py

from tools.sequencemanipulator import SequenceManipulator

class RotMixin:
    """
    Mixin that provides ROT‐style (Caesar) rotation.

    When called with an integer `shift`, returns a new SequenceManipulator
    where the underlying sequence is rotated by `shift` positions
    via SequenceManipulator.rotate_by().

    Usage:
        class SomeEngine(RotMixin):
            def __init__(self, sequence: SequenceManipulator[str]):
                self.sequence = sequence

        engine = SomeEngine(seq)
        new_seq = engine(13)  # SequenceManipulator rotated by 13
    """

    def __call__(self, shift: int) -> SequenceManipulator[str]:
        if not hasattr(self, 'sequence'):
            raise AttributeError(
                "RotMixin requires 'self.sequence' to be set to a SequenceManipulator instance before calling."
            )
        if len(self.sequence) == 0:
            raise ValueError("Cannot rotate an empty sequence in RotMixin.")

        # Delegate to rotate_by for positive/negative shifts
        return self.sequence.rotate_by(shift)

