import unittest
import document_transformer
import bigramTokenizer
import documents

def getInput(id: str, text: str):
    transformer = document_transformer.BigramSearchDocumentTransformer(bigramTokenizer.BigramTokenizer())
    document = documents.InputDocument(doc_id=id, text=text)
    return transformer.transform_document(doc=document)

def getOutput(id: str, texts: [str]):
    document = documents.TransformedDocument(doc_id=id, tokens=texts)
    return document

class MyTestCase(unittest.TestCase):



    def test1(self):
        self.assertEqual(getInput(id='1', text='to be or not to be'), getOutput(id='1', texts=['to be', 'be or', 'or not', 'not to', 'to be']))

if __name__ == '__main__':
    unittest.main()
