# message_bit.py

class MessageBit:
    """
    A lightweight wrapper for text to allow clean manipulation and iteration.

    Provides:
        - Iteration over characters.
        - Indexing and slicing support.
        - Grouping, padding, and whitespace stripping as methods.
    """

    def __init__(self, text: str):
        """
        Initialize the MessageBit with a given text string.

        Args:
            text (str): The text to wrap.
        """
        self._text = text

    def __iter__(self):
        """
        Iterate over the characters of the text.

        Returns:
            Iterator over characters.
        """
        return iter(self._text)

    def __len__(self):
        """
        Get the length of the text.

        Returns:
            int: Number of characters in the text.
        """
        return len(self._text)

    def __getitem__(self, index):
        """
        Get character(s) at a specific index or slice.

        Args:
            index (int or slice): The position or slice.

        Returns:
            str: Single character or substring.
        """
        return self._text[index]

    def __str__(self):
        """
        Return the text as a string.

        Returns:
            str: The underlying text.
        """
        return self._text

    def as_list(self) -> list:
        """
        Return the text as a list of characters.

        Returns:
            list: List of individual characters.
        """
        return list(self._text)

    def group(self, size: int = 5) -> str:
        """
        Split the text into groups of specified size, separated by spaces.

        Args:
            size (int): Size of each group.

        Returns:
            str: Grouped string.
        """
        return ' '.join(self._text[i:i + size] for i in range(0, len(self._text), size))

    def pad(self, target_length: int, pad_char: str = 'X') -> "MessageBit":
        """
        Pad the text to the target length using the specified character.

        Args:
            target_length (int): The desired total length.
            pad_char (str): The character used for padding.

        Returns:
            MessageBit: New instance with padded text.
        """
        return MessageBit(self._text.ljust(target_length, pad_char))

    def without_spaces(self) -> "MessageBit":
        """
        Return a new MessageBit instance with all spaces removed.

        Returns:
            MessageBit: Instance without spaces.
        """
        return MessageBit(''.join(self._text.split()))

