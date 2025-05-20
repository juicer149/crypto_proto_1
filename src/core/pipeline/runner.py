# core/cipher_pipeline.py

class CipherPipeline:
    """
    A pipeline that apply a list of engines on a text.
    Every engine have to implement get_substitution_for_position(pos)
    """

    def __init__(self, engines):
        self.engines = engines

    def encrypt(self, text):
        for engine in self.engines:
            result = []
            for i, char in enumerate(text):
                sub_map = engine.get_substitution_for_position(i)
                result.append(sub_map.get(char, char))
            text = ''.join(result)
        return text
