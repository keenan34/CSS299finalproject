#obamna
#the one piece isn't real
#can we get much higher
#suh dude

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
#-one way we can identify them is finding bigrams that have - (dashes) in them i.e. pre-school
#Rank Bigrams based on their relevance to the query
