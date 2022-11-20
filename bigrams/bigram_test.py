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
        self.assertEqual(getInput(id='1', text='to be or not to be'),
                         getOutput(id='1', texts=['to be', 'be or', 'or not', 'not to', 'to be']))

    def test2(self):
        self.assertEqual(getInput(id='123', text = " This is the best place to learn Data Science Learner This is the best place to learn Data Science Learner"),
                         getOutput(id='123', texts=['this is', 'is the', 'the best', 'best place', 'place to', 'to learn', 'learn data', 'data science', 'science learner', 'learner this', 'this is', 'is the', 'the best', 'best place', 'place to', 'to learn', 'learn data', 'data science', 'science learner']))

    def test3(self):
        self.assertEqual(getInput(id='1', text="The best performance can bring in sky high success."),
                         getOutput(id='1', texts=['the best', 'best performance', 'performance can', 'can bring', 'bring in', 'in sky', 'sky high', 'high success']))
if __name__ == '__main__':
    unittest.main()
