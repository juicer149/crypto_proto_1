from typing import List, Dict, Any
from load_yaml import load_yaml

class AlphabetProviderMixin:
    """
    Laddar alla alfabet från config/charsets.yaml och
    returnerar en lista str-tecken för valt språk.
    """

    def __init__(self, config_path: str = "config/charsets.yaml"):
        data = load_yaml(config_path)
        if "alphabets" not in data:
            raise KeyError(f"'alphabets' key missing in {config_path}")
        self._alphabets_config: Dict[str, Any] = data["alphabets"]

    def get_alphabet(self, language: str = "en") -> List[str]:
        """
        Bygger upp en lista av tecken för 'language' enligt:
          - 'ranges': intervall av Unicode-koder
          - 'extras': enskilda Unicode-koder
        """
        cfg = self._alphabets_config.get(language)
        if cfg is None:
            raise ValueError(f"Unknown language: {language!r}")

        chars: List[str] = []
        # Hantera intervall
        for start, end in cfg.get("ranges", []):
            chars.extend(chr(i) for i in range(start, end + 1))
        # Hantera enstaka extras
        for code in cfg.get("extras", []):
            chars.append(chr(code))
        return chars
