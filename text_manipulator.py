# text_manipulator.py


class TextManipulator:


    @staticmethod
    def normalize(
            text            : str,
            keep_case       : bool  = False,
            allow_nonalpha  : bool  = False,
            ) -> str:
        """
        Normalize text by:
          - Optionally preserving case
          - Optionally allowing non-alphabetic characters
          - Otherwise removing everything except A–Z/a–z

        Args:
            text (str)              : Input string.
            keep_case (bool)        : If False, convert to upper case.
            allow_nonalpha (bool)   : If True, preserve characters like digits, punctuation.

        Returns:
            str: The normalized string.
        """
        
        if not keep_case:
            text = text.upper()

        if not allow_nonalpha:
            text = ''.join(char for char in text if char.isalpha())

        return text


    @staticmethod
    def remove_spaces(text: str) -> str:
        """Remove all whitespace characters from text."""
        return ''.join(text.split())


    @staticmethod
    def pad_to_length(
            text    : str,
            length  : int,
            pad_char: str   = 'X'
            ) -> str:
        """
        Pad text on the right with `pad_char` until it reaches `length`.

        If text is already `length` or longer, it's returned unchanged.
        """

        if len(text) >= length:
            return text 
        return text + pad_char * (length - len(text))


    @staticmethod
    def group_text(
            text    : str,
            size    : int   = 5
            ) -> str:
        """
        Split text into groups of given size.

        Args:
            text (str): Input string.
            size (int): Group size.

        Returns:
            str: Groups separated by spaces.
        """

        if size <= 0:
            return text

        return ' '.join(text[i:i + size] for i in range(0, len(text), size))


    @classmethod
    def format_text(
            cls,
            text: str,
            remove_spaces: bool = False,
            keep_case: bool = False,
            allow_nonalpha: bool = False,
            group: bool = False,
            group_size: int = 5,
            pad: bool = False,
            pad_char: str = 'X'
            ) -> str:
        """
        Apply a sequence of text transformations:
            1. Normalize (case, non-alpha)
            2. Optionally remove spaces
            3. Optionally pad to a multiple of group_size
            4. Optionally group into blocks

        Args:
            text (str): Input string.
            remove_spaces (bool): Remove spaces if True.
            keep_case (bool): Preserve original case if True.
            allow_nonalpha (bool): Keep non-alpha chars if True.
            group (bool): Group text if True.
            group_size (int): Size of each group.
            pad (bool): Pad to full group if True.
            pad_char (str): Character to use for padding.

        Returns:
            str: Transformed text.
        """
        result = cls.normalize(text, keep_case, allow_nonalpha)

        if remove_spaces:
            result = cls.remove_spaces(result)

        if pad and group and group_size > 0:
            remainder = len(result) % group_size
            if remainder:
                result = cls.pad_to_length(result, len(result) + (group_size - remainder), pad_char)

        if group and group_size > 0:
            result = cls.group_text(result, group_size)

        return result
