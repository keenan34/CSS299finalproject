from unittest import TestCase
import bigramTokenizer


class Test(TestCase):
    def test_tokenize__splits_words(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('word1 word2'), ['word1', 'word2'])

    def test_tokenize__comma(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('For now, we are here'), ['for', 'now', 'we', 'are', 'here'])

    def test_tokenize__period(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('For now, we are here.'), ['for', 'now', 'we', 'are', 'here'])

    def test_tokenize__other_non_word_chars(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('10% of $5 is 50 c'), ['10', 'of', '5', 'is', '50', 'c'])

    def test_tokenize__apostrophe(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('He said \'Isn\'t O\'Brian the best?\''),
                         ['he', 'said', 'isn\'t', 'o\'brian', 'the', 'best'])

    def test_tokenize__ellipsis(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('More...'), ['more'])

    def test_tokenize__corpus(self):
        self.assertEqual(bigramtokenizer.BigramTokenizer.tokenize('OBJECTIVE: This retrospective chart review describes the epidemiology and clinical features of 40 patients with culture-proven Mycoplasma pneumoniae infections at King Abdulaziz University Hospital, Jeddah, Saudi Arabia. METHODS: Patients with positive M. pneumoniae cultures from respiratory specimens from January 1997 through December 1998 were identified'), ['more'])

