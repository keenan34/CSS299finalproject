import abc
from abc import ABC
from typing import Dict, List
from collections import Counter
from documents import InputDocument, TransformedDocument

class CounterBasedTextCounter():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def count_words(self, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(self.tokenizer.tokenize(text))
        return counts


class DocumentTransformer(ABC):
    """
    Text Transformation component of the Index Process.

    Text normalization and tokenization is expected to be part of this component.
    """
    @abc.abstractmethod
    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        pass


class BigramSearchDocumentTransformer(DocumentTransformer):
    """
    An DocumentTransformer implementation that runs the supplied tokenizer.
    """
    def __init__(self, tokenizer):
        """
        :param tokenizer: A tokenizer instance that will be used in document transformation.
        """
        self.tokenizer = tokenizer


    def count_total_words(self, texts_list: List[str]) -> Counter:
        counts = Counter()
        counter = CounterBasedTextCounter(tokenizer=self.tokenizer)
        for text in texts_list:
            counts.update(counter.count_words(text))
        return counts

    def compute_stopwords(self, words: [str]) -> [str]:
        counts = self.count_total_words(words)
        stopwords = set()
        for count in counts.most_common(20):
            counter = 0
            for word in words:
                if count[0] in word:
                    counter += 1
            if counter >= 9:
                stopwords.add(count[0])
        return stopwords

    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        """
        Creates TransformedDocument from the given InputDocument by tokenizing its text.

        Uses the tokenizer instance supplied in the constructor.
        :param doc: The InputDocument to be transformed.
        :return: The transformed document
        """
        tokens = self.tokenizer.tokenize(doc.text)
        stopwords = self.compute_stopwords(words=tokens)
        digrams = list()
        for i in range(len(tokens) - 1):
            if tokens[i] not in stopwords and tokens[i+1] not in stopwords: digrams.append(tokens[i] + ' ' + tokens[i + 1])
        return TransformedDocument(doc_id=doc.doc_id, tokens=digrams)
