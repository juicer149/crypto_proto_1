# engines/plugboard.py

class PlugboardEngine:
    """
    Simple plugboard (static substitutionalmap).
    """

    def __init__(self, substitution_map):
        self._map = substitution_map

    def get_substitution_for_position(self, pos):
        return self._map
