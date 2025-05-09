from abc import ABC, abstractmethod


class BaseCipher(ABC):
    """
    Minimal abstrakt klass; innehåller bara normalize
    och signatur för encrypt/decrypt.
    """


    @staticmethod
    def _normalize(text: str) -> str:
        return ''.join(ch for ch in text if ch.isalpha()).upper()


    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Ta en klartext‐sträng och returnera krypterad text."""
        ...


    @abstractmethod
    def decrypt(self, text: str) -> str:
        """Ta en krypterad sträng och returnera klartext."""
        ...
