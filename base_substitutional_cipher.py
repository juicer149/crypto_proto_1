from .base_cipher import BaseCipher
from .alphabet import Alphabet


class BaseSubstitutionalCipher(BaseCipher):
    """
    Base class for substitution ciphers using character alphabets.

    This class provides the foundational logic for ciphers based on 
    substituting one alphabet with another. It automatically loads a 
    base alphabet from a YAML configuration file using the Alphabet class.

    Features:
        - Loads a base alphabet from YAML.
        - Provides rotation of the base alphabet (e.g., Caesar/ROT shifts).
        - Builds substitution maps between two alphabets of equal length.

    Attributes:
        base_alphabet (Alphabet): The base alphabet used for substitutions.
    """


    def __init__(
            self,
            language: str = "en",
            config_path: str = "config/charsets.yaml"
    ):
        """
        Initialize the substitution cipher with a base alphabet.

        Args:
            language (str): The language key to load the alphabet for.
            config_path (str): Path to the YAML file containing alphabet definitions.
        """
        super().__init__()
        self.base_alphabet: Alphabet = Alphabet.from_config(language, config_path)


    def rotate_alphabet(self, shift: int) -> Alphabet:
        """
        Return a rotated version of the base alphabet.

        Args:
            shift (int): Number of positions to rotate by.

        Returns:
            Alphabet: A new Alphabet instance rotated by the specified shift.
        """
        return self.base_alphabet * shift


    def build_substitution_map(self, other_alphabet: Alphabet) -> dict:
        """
        Build a substitution map from the base alphabet to the provided alphabet.

        Args:
            other_alphabet (Alphabet): The target alphabet to map to.

        Returns:
            dict: A mapping from each character in the base alphabet to the corresponding character in the target alphabet.

        Raises:
            ValueError: If the two alphabets do not have the same length.
        """
        return self.base_alphabet.substitution_map(other_alphabet)
 
