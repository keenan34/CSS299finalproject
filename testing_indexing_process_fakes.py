from indexing_process import *

class FakeDocumentCollection(DocumentCollection):
    def __init__(self, docs: List[InputDocument]):
        self.docs = docs

    @classmethod
    def from_str_list(cls, docs: List[str]):
        return cls([InputDocument(doc_id=str(i), text=doc) for i, doc in enumerate(docs)])

    def __iter__(self):
        return self.docs.__iter__()

    def get_doc(self, doc_id):
        return next((d for d in self.docs if d.doc_id == doc_id), None)

    def get_docs(self, doc_ids: Iterable[str]):
        return FakeDocumentCollection([d for d in self.docs if d.doc_id in doc_ids])


class FakeDocumentSource(DocumentSource):
    def __init__(self, doc_collection: DocumentCollection):
        self.doc_collection = doc_collection

    def read(self):
        return self.doc_collection


class FakeDocumentTransformer(DocumentTransformer):
    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        return TransformedDocument(doc.doc_id, doc.text.split())


