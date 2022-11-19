import abc
from abc import ABC
from typing import Dict, List
from collections import defaultdict, Counter
import json
import re

class TextCounter(ABC):
    @staticmethod
    @abc.abstractmethod
    def count_characters(text: str) -> Dict[str, int]:
        pass


class DictBasedTextCounter(TextCounter):
    @staticmethod
    def count_characters(text: str) -> Dict[str, int]:
        counts = dict()
        for char in text:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
        return counts


class DefaultDictBasedTextCounter(TextCounter):
    @staticmethod
    def count_characters(text: str) -> Dict[str, int]:
        counts = defaultdict(int)
        for char in text:
            counts[char] += 1
        return counts

class tokenizer():
    def tokenize(text: str) -> List[str]:
        text = re.sub(r'[^\w\s\']', '', text)
        initial = re.sub(r'(\W)', r' \1 ', text.lower())
        adjusted = re.sub(r'(\w) \' (\w)', r"\1'\2", initial)
        final = re.sub(r' \' ', '', adjusted)
        return final.split()


class CounterBasedTextCounter(TextCounter):
    @classmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(text)
        return counts

    def count_words(self, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(tokenize(text))
        return counts

def get_file(filename: str):
    with open(filename) as fp:
        return json.load(fp)

def count_total_words(texts_list: List[str]) -> Counter:
    counts = Counter()
    counter = CounterBasedTextCounter()
    for text in texts_list:
        counts.update(counter.count_words(text))
    return counts


# [d['init_text'] for d in data if d['init_text']]
def get_texts_from_data(data):
    output = []
    for d in data:
        if d['init_text']:
            text = d['init_text']
            output.append(text)
    return output

class BigramDocumentTransformer():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def transform_document(self, doc: [str]) -> [str]:
        tokens = self.tokenizer.tokenize(doc);
        digrams = list()
        for i in range(len(tokens) - 1):
            digram = tokens[i] + ' ' + tokens[i+1]
            digrams.append(digram)
        return digrams

def compute_document_counts(documents: [str]):
    document_counts = Counter()
    for document in documents:
        document = BigramDocumentTransformer(tokenizer=tokenizer).transform_document(document)
        document_counts.update(document)
    for document_count in document_counts:
        if document_counts[document_count] > 10:
            document_counts[document_count] = 10
    return document_counts


def compute_stopwords(words: [str]) -> [str]:
    counts = count_total_words(words)
    stopwords = set()
    for count in counts.most_common(20):
        counter = 0
        for word in words:
            if count[0] in word:
                counter += 1
        if counter >= 9:
            stopwords.add(count[0])
    return stopwords


def get_best_terms(texts: [str], stopwords: [str]):
    counts = [Counter(tokenizer.tokenize(text)) for text in texts]
    best_terms = []
    for count in counts:
        for stopword in stopwords:
            del count[stopword]
        best_terms.append(count.most_common(10))
    return best_terms


def create_inverted_index(texts: [str]):
    output_dict = defaultdict(set)
    for i in range(len(texts)):
        for word in tokenizer.tokenize(texts[i]):
            output_dict[word].add(i)
    return output_dict


def search_2_words(word1: str, word2: str, index: set):
    return index[word1].intersection(index[word2])



def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


documents = get_texts_from_data(get_file('wiki_small.json'))
with open('bigrams_counts.json', 'w') as fp:
    json.dump(compute_document_counts(documents),fp)