#obamna
#the one piece isn't real
#can we get much higher
#suh dude
import nltk

#Got to use this is download nltk bigram stuff
#nltk.download()

#word_data="The best performance can bring in sky high success."
#nltk_tokens=nltk.word_tokenize(word_data)
#print(list(nltk.bigrams(nltk_tokens)))

#THE GOD CODE
from nltk.tokenize import word_tokenize
# text = "to be or not to be"
# tokens = nltk.word_tokenize(text)
# bigrm = nltk.bigrams(tokens)
# print(*map(' '.join, bigrm), sep=', ')
#corpus_text=corpus.jsonl.read();
# tokens = nltk.word_tokenize(text)
# bigrm = nltk.bigrams(tokens)
# print(*map(' '.join, bigrm), sep=', ')
text=" This is the best place to learn Data Science Learner This is the best place to learn Data Science Learner"
tokens = nltk.word_tokenize(text)
bigrams = nltk.bigrams(tokens)
frequency = nltk.FreqDist(bigrams)
for key,value in frequency.items():
    print(key,value)
#to be, be or, or not, not to, to be
#word_data="The best performance can bring in sky high success."
#nltk_tokens=nltk.word_tokenize(word_data)
#print(list(nltk.bigrams(nltk_tokens)))
text=" This is the best place to learn Data Science Learner This is the best place to learn Data Science Learner"
tokens = nltk.word_tokenize(text)
bigrams = nltk.bigrams(tokens)
frequency = nltk.FreqDist(bigrams)
for key,value in frequency.items():
    print(key,value)

#Tokenize Document: break up the text into strings that contain individual words
 document_collection = source.read()
        # Create an empty index. Documents will be added one at a time.
        index = self.indexer.create_index()
        for doc in document_collection:
            # Transform and index the document.
            transformed_doc = self.document_transformer.transform_document(doc)
            index.add_document(transformed_doc)
        return index
#Filter stop words: filter out all stopwords from the tokenized document i.e. words like and, or, not, etc.
def compute_stopwords(texts: List[str]) -> Set[str]:
    doc_counts = compute_document_counts(texts)
    total_counts = count_total_words(texts)
    stopwords = set()
    for w, _ in total_counts.most_common(20):
        if doc_counts[w] >= 9:
            stopwords.add(w)
    return stopwords
#Identify Bigrams: find all bigrams from filtered tokenize documents AND find all bigrams in the query (in the search)
def search(self, query: Query) -> SearchResults:
        match_scores = defaultdict(float)
        match_counts = defaultdict(int)
        for term in query.terms:
            if term not in self.term_to_doc_id_and_frequencies:
                return SearchResults([])
            idf = inverse_document_frequency(self.doc_counts[term], self.number_of_documents)
            for doc_id, tf in self.term_to_doc_id_and_frequencies[term]:
                match_counts[doc_id] += 1
                match_scores[doc_id] += tf * idf
        match_scores = {doc_id: score
                        for doc_id, score in match_scores.items()
                        if match_counts[doc_id] == len(query.terms)}
        sorted_results = sorted(match_scores.keys(), key=match_scores.get)
        return SearchResults(sorted_results[0:query.num_results])
#-one way we can identify them is finding bigrams that have - (dashes) in them i.e. pre-school

#Document counts
def compute_document_counts(texts: List[str]) -> Counter:
    counts = Counter()
    for text in texts:
        # unique_tokens = set(tokenize(text))
        # for token in unique_tokens:
        #     counts[token] += 1
        counts.update(set(tokenize(text)))
    return counts
#Counter based text counters
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
#Rank Bigrams based on their relevance to the query
