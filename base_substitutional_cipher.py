from typing             import List, Dict

from .base_cipher       import BaseCipher
from .alphabet_provider import AlphabetProviderMixin
from .alphabet_handler  import AlphabetHandlerMixin


class BaseSubstitutionalCipher(
        BaseCipher,
        AlphabetProviderMixin,
        AlphabetHandlerMixin
):
    """
    För chiffer som bygger på substitution av ett alfabet mot ett annat.
    Laddar automatiskt base_alphabet från YAML och tillhandahåller
    rotate_alphabet + build_substitution_map.
    """

    def __init__(
            self,
            language    : str = "en",
            config_path : str = "config/charset.yaml"
    ):
        # Init för alfabet-provider
        AlphabetProviderMixin.__init__(self, config_path)
        # Basalfabetet för substitutioner
        self.base_alphabet: List[str] = self.get_alphabet(language)
