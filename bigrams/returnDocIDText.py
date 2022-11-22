import document_transformer
import json
from index import SearchResults

#STILL WORKING ON IMPLEMENTING
# given a doc ID - search jsonl file for the json file that contains that ID
# and return (or get and store) it's URL

def gettext(self):
    r = open('corpus.jsonl')

    # returns JSON object as
    # a dictionary
    data = json.load(r)

    # Iterating through the json
    # list

    # we need to get specific ID returned by searchBigrams.py
    # and use that to add text to what searchBigrams returns
    # key = SearchResults.result_doc_ids
    for SearchResults.result_doc_ids in data:
        to_print = data['text']
        print('Your relevant documents are:')
        print(to_print)

    # Closing file
    r.close()

    # for(doc.doc_id in corpus.)
