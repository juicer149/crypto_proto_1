# cipher_catalog.py
import warnings
from typing import Type, Dict


# Global cipher registry : name -> class
CIPHER_CATALOG: Dict[str, Type] = {}


def register_cipher(name: str):
    """
    Decorator that registers a cipher class under the given 'name'.
    If 'name' is already registered, emits a UserWarning and does nothing.

    Example:
        from cipher_catalog import register_cipher

        @register_cipher('caesar')
        class CaesarCipher:
        ...
    """

    def decorator(cls: Type) -> Type:
        
        if name in CIPHER_CATALOG:
            warnings.warn(
                    f"Cipher '{name}' is already registered; ignoring new registration",
                    category    = UserWarning, 
                    stacklevel  = 2,
            )
            return cls # no changes, keeping the existing class in catalog 
        
        # First-time registration
        CIPHER_CATALOG[name] = cls
        return cls

    return decorator
