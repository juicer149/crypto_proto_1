# cipher_factory.py
from typing import Any

from cipher_catalog import CIPHER_CATALOG
from load_yaml import load_yaml


def create_cipher(
        name: str,
        config_path: str = "config/cipher.yaml",
        **overrides
) -> Any:
    """
    Factory that creates a cipher instance by 'name'.
    Merges optional config from YAML with provides arguments (**overrides).

    Args:
        name (str): Name of the cipher (must be registered in CIPHER_CATALOG).

        config_path (str): Path to YAML file with default cipher parameters.
            - tech dept: create a dataclass that stores file names

        **overrides: Any keywordargument overrides YAML/defaults.
            Example: for ROT which by default is 13 or for caesar is 3 can be
                     overwritten if the user have specified shifts.

    Returns:
        Instance of the cipher class.

    Raises:
        ValueError: If cipher 'name' is unknown.
    """

    if name not in CIPHER_CATALOG:
        raise ValueError(f"Unknown cipher: {name!r}")

    cipher_cls = CIPHER_CATALOG[name]

    # Loads default params from yaml 
    config_data = load_yaml(config_path).get(name, {}) 

    # Merge CLI overrides on top of YAML
    merged_args = {**config_data, **overrides} 

    # Create and return the cipher instance
    return cipher_cls(**merged_args)
