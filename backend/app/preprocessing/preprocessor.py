import re

class PreprocessedRequirement:

    def __init__(self, text: str):

        self.original = text

        self.normalized = text.lower().strip()

        self.tokens = self._tokenize(self.normalized)


    def _tokenize(self, text: str):

        return re.findall(r"\b\w+\b", text)