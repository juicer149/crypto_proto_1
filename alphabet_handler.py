class AlphabetHandlerMixin:
    """
    Innehåller rena verktyg för att transformera ett alfabet:
      - rotate_alphabet()
      - build_substitution_map()
    """

    def rotate_alphabet(self, alphabet: list[str], shift: int) -> list[str]:
        """
        Returnerar en *ny* lista där elementen är roterade shift steg.
        """
        shift = shift % len(alphabet)
        return alphabet[shift:] + alphabet[:shift]

    def build_substitution_map(
        self,
        base: list[str],
        target: list[str]
    ) -> dict[str, str]:
        """
        Mapper varje tecken i base till motsvarande tecken i target.
        Höjer ValueError om längderna skiljer.
        """
        if len(base) != len(target):
            raise ValueError(
                f"Alphabets must be same length, got {len(base)} and {len(target)}"
            )
        return dict(zip(base, target))

