# text_manipulator.py

from message_bit import MessageBit


class TextManipulator:
    """
    Utility class for text preprocessing.
    Returns text wrapped in a MessageBit object for safe iteration and manipulation.
    """

    @staticmethod
    def normalize(
        text: str,
        keep_case: bool = False,
        allow_nonalpha: bool = False,
    ) -> MessageBit:
        """
        Normalize text by converting to uppercase (if not keep_case)
        and removing all non-alphabetic characters (unless allow_nonalpha is True).

        Args:
            text (str): Input string.
            keep_case (bool): If False, convert to upper case.
            allow_nonalpha (bool): If False, remove all non-alpha characters.

        Returns:
            MessageBit: The normalized text as a MessageBit object.
        """
        if not keep_case:
            text = text.upper()

        if not allow_nonalpha:
            text = ''.join(char for char in text if char.isalpha())

        return MessageBit(text)

    @staticmethod
    def remove_spaces(bit: MessageBit) -> MessageBit:
        """
        Remove all spaces from the given MessageBit.

        Args:
            bit (MessageBit): The MessageBit instance.

        Returns:
            MessageBit: New instance without spaces.
        """
        return MessageBit(str(bit).replace(" ", ""))

    @staticmethod
    def pad_to_length(bit: MessageBit, length: int, pad_char: str = 'X') -> MessageBit:
        """
        Pad the MessageBit to the target length using pad_char.

        Args:
            bit (MessageBit): The MessageBit instance.
            length (int): Desired length.
            pad_char (str): Character to pad with.

        Returns:
            MessageBit: Padded instance.
        """
        return bit.pad(length, pad_char)

    @staticmethod
    def group_text(bit: MessageBit, size: int = 5) -> str:
        """
        Split the text into groups of given size, separated by spaces.

        Args:
            bit (MessageBit): The MessageBit instance.
            size (int): Group size.

        Returns:
            str: Grouped string.
        """
        return bit.group(size)

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
    ) -> MessageBit:
        """
        Apply a full sequence of text transformations:
            1. Normalize (case, non-alpha handling).
            2. Optionally remove spaces.
            3. Optionally pad to multiple of group_size.
            4. Optionally group into blocks (returned as str using .group()).

        Args:
            text (str): Input text.
            remove_spaces (bool): If True, remove all spaces.
            keep_case (bool): If False, convert to uppercase.
            allow_nonalpha (bool): If False, remove all non-alpha characters.
            group (bool): If True, the resulting text can be grouped (via .group()).
            group_size (int): Group size for grouping.
            pad (bool): If True, pad to multiple of group_size.
            pad_char (str): Padding character.

        Returns:
            MessageBit: Processed MessageBit object.
        """
        bit = cls.normalize(text, keep_case, allow_nonalpha)

        if remove_spaces:
            bit = cls.remove_spaces(bit)

        if pad and group and group_size > 0:
            remainder = len(bit) % group_size
            if remainder:
                bit = cls.pad_to_length(bit, len(bit) + (group_size - remainder), pad_char)

        if group and group_size > 0:
            # OBS: This will return still a MessageBit, not grouped string here.
            # Grouping should be explicitly called via bit.group() later.
            pass  # Keep the object as is

        return bit
