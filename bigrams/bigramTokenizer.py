from typing import List
import re
import abc
from abc import ABC

class Tokenizer(ABC):
    @abc.abstractmethod
    def tokenize(self, text: str):
        pass


class BigramTokenizer(Tokenizer):
    def tokenize(self, text: str) -> List[str]:
        text = re.sub(r'[^\w\s\']', '', text)
        initial = re.sub(r'(\W)', r' \1 ', text.lower())
        adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
        final = re.sub(r' \' ', '', adjusted)
        return final.split()
