import abc
import json
import math
from abc import ABC
from collections import defaultdict, Counter

from documents import TransformedDocument
from search_api import Query, SearchResults


class Index(ABC):
    """
    Index that is the final output of the Indexing Process and the main source for Query Process.
    """
    @abc.abstractmethod
    def add_document(self, doc: TransformedDocument) -> None:
        pass

    @abc.abstractmethod
    def search(self, query: Query) -> SearchResults:
        pass

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def write(self):
        pass


class Indexer(ABC):
    """
    Factory class for Index
    """
    @abc.abstractmethod
    def create_index(self) -> Index:
        pass


class NaiveIndex(Index):
    def __init__(self, filename: str):
        self.filename = filename
        self.docs = []

    def add_document(self, doc: TransformedDocument) -> None:
        self.docs.append(doc)

    def search(self, query: Query) -> SearchResults:
        query_terms = set(query.terms)
        matching_doc_ids = []
        for doc in self.docs:
            if query_terms.issubset(doc.tokens):
                matching_doc_ids.append(doc.doc_id)
        return SearchResults(result_doc_ids=matching_doc_ids)

    def read(self):
        with open(self.filename) as fp:
            records = json.load(fp)
        # records = [{'doc_id': "12", 'tokens': ['a', 'b']}, {'doc_id': "13", 'tokens': ['c', 'd']}]
        # self.docs = []
        # for record in records:
        #     self.docs.append(TransformedDocument(doc_id=record['doc_id'], tokens=record['tokens']))
        self.docs = [TransformedDocument(doc_id=record['doc_id'], tokens=record['tokens'])
                     for record in records]

    def write(self):
        with open(self.filename, 'w') as fp:
            json.dump([{'doc_id': doc.doc_id, 'tokens': doc.tokens} for doc in self.docs], fp)


class NaiveIndexer(Indexer):
    def __init__(self, index_filename):
        self.index_filename = index_filename

    def create_index(self) -> Index:
        return BigramIndexWithFrequencies(self.index_filename)


def term_frequency(term_count, document_length):
    return term_count / document_length


def inverse_document_frequency(term_document_count, number_of_document):
    return math.log(number_of_document / term_document_count)


class BigramIndexWithFrequencies(Index):
    def __init__(self, filename):
        self.filename = filename
        self.number_of_documents = 0
        # dict mapping a term to a list of pairs (doc_id, term_frequency)
        self.term_to_doc_id_and_frequencies = defaultdict(list)
        # Count of documents each term occurs in.
        self.doc_counts = Counter()

    def add_document(self, doc: TransformedDocument) -> None:
        self.number_of_documents += 1
        term_counts = Counter(doc.tokens)
        for term, count in term_counts.items():
            self.doc_counts[term] += 1
            tf = term_frequency(count, len(doc.tokens))
            self.term_to_doc_id_and_frequencies[term].append((doc.doc_id, tf))

    def read(self):
        with open(self.filename) as fp:
            record = json.loads(fp.readline())
            self.number_of_documents = record['number_of_documents']
            self.term_to_doc_id_and_frequencies = defaultdict(list)
            self.doc_counts = Counter()
            for line in fp:
                record = json.loads(line)
                term = record['term']
                self.doc_counts[term] = record['documents_count']
                self.term_to_doc_id_and_frequencies[term] = [
                    (sub_record['doc_id'], sub_record['tf']) for sub_record in record['index']]

    def write(self):
        with open(self.filename, 'w') as fp:
            metadata = {'number_of_documents': self.number_of_documents}
            fp.write(json.dumps(metadata) + '\n')
            for term, doc_count in self.doc_counts.items():
                record = {
                    'term': term,
                    'documents_count': doc_count,
                    'index': [{'doc_id': doc_id, 'tf': tf}
                              for doc_id, tf in self.term_to_doc_id_and_frequencies[term]]
                }
                fp.write(json.dumps(record) + '\n')

    def search(self, bigram: Query) -> SearchResults:
        match_scores = defaultdict(float)
        match_counts = defaultdict(int)
        if bigram not in self.term_to_doc_id_and_frequencies:
            return SearchResults([])
        idf = inverse_document_frequency(self.doc_counts[bigram], self.number_of_documents)
        for doc_id, tf in self.term_to_doc_id_and_frequencies[bigram]:
            match_counts[doc_id] += 1
            match_scores[doc_id] += tf * idf
        sorted_results = sorted(match_scores.keys(), key=match_scores.get)
        return SearchResults(sorted_results)