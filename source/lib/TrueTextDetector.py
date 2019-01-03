from lib import io_library
from lib.Characters import LETTERS_AND_SPACE


def load_dictionary(file: str) -> set:
    """
    Function to load dictionary file's words into a set

    :param file: path to dictionary file, must be json
    :return: set of dictionary words
    :rtype: set
    """
    dictionary = io_library.reader(file, 'j')

    return {word.upper() for word in dictionary}


def is_true_text(string: str, words: set, word_percentage: int = 20, letter_percentage: int = 85) -> bool:
    """
    Function to determine if the given string is proper text or not
    you can adjust sensitivity and overwrite default threshold percentage

    :param string: string to be examined
    :param words: set of words
    :param word_percentage: minimum words threshold
    :param letter_percentage: minimum letter in string threshold
    :rtype: bool
    """
    words_match = get_words_count(string, words) * 100 >= word_percentage
    letters_match = len(remove_non_letters(string)) / len(string) * 100 >= letter_percentage

    return words_match and letters_match


def get_words_count(string: str, words: set):
    """
    Function to count matches between words in
    a string and a dictionary set

    :param string: string to be examined
    :param words: dictionary set
    :return: ratio matches/all words
    """
    string = string.upper()
    string = remove_non_letters(string)
    possible_words = string.split()
    if not possible_words:
        return 0.0
    matches = 0
    for word in possible_words:
        if word in words:
            matches += 1

    return matches / len(possible_words)


def remove_non_letters(string: str):
    """
    Function to remove everything but alphabet
    letters from a given string

    :param string: string
    :return: cleaned string
    """

    letters_only = [symbol for symbol in string if symbol in LETTERS_AND_SPACE]

    return ''.join(letters_only)
