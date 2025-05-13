# cipher_base-py

from abc import ABC, abstractmethod

from text_manipulator import TextManipulator


class BaseCipher(ABC):
    """
    Abstract base class for ciphers.
    Uses TextManipulator as a utility instance.
    """

    manipulator = TextManipulator # Class reference; easy to replace or mock.


    @abstractmethod
    def encrypt(self, text: str) -> str:
        ...


    @abstractmethod
    def decrypt(self, text: str) -> str:
        ...
