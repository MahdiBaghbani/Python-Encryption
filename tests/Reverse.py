import unittest
from sources.Reverse import reverse


class ReverseModule(unittest.TestCase):
    def test_empty_string(self):
            self.assertEqual(reverse(''), '')

    def test_a_word(self):
            self.assertEqual(reverse('robot'), 'tobor')

    def test_a_capitalized_word(self):
            self.assertEqual(reverse('Ramen'), 'nemaR')

    def test_a_sentence_with_punctuation(self):
            self.assertEqual(reverse('I\'m hungry!'), '!yrgnuh m\'I')

    def test_a_palindrome(self):
            self.assertEqual(reverse('racecar'), 'racecar')


if __name__ == '__main__':
    unittest.main()
