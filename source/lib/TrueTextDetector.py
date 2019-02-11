from lib import io_library
from lib.Characters import LETTERS_AND_SPACE


def load_dictionary(dictionary_file_path: str) -> set:
    """
    Function to load dictionary file's words into a set

    :param dictionary_file_path: path to dictionary file, must be json
    :return: set of dictionary words
    :rtype: set
    """

    # check inputs
    if not type(dictionary_file_path) == str:
        raise TypeError("Argument 'dictionary_file_path' of this function must be of type string.\n")

    dictionary = io_library.reader(dictionary_file_path, 'j')

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

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")
    if not type(words) == set:
        raise TypeError("Argument 'words' of this function must be of type set.\n")
    if not (type(word_percentage) == int and type(letter_percentage) == int):
        raise TypeError("Arguments 'word_percentage' and 'letter_percentage' of this function must be of type "
                        "integer.\n")

    # create booleans based on limits
    words_match = get_words_count(string, words) * 100 >= word_percentage
    letters_match = len(remove_non_letters(string)) / len(string) * 100 >= letter_percentage
    # return final result
    return words_match and letters_match


def get_words_count(string: str, words: set):
    """
    Function to count matches between words in
    a string and a dictionary set

    :param string: string to be examined
    :param words: dictionary set
    :return: ratio matches/all words
    """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")
    if not type(words) == set:
        raise TypeError("Argument 'words' of this function must be of type set.\n")

    # preprocessed string
    string = string.upper()
    string = remove_non_letters(string)
    possible_words = string.split()

    if not possible_words:
        return 0.0
    matches = 0
    for word in possible_words:
        if word in words:
            matches += 1

    # return percentage
    return matches / len(possible_words)


def remove_non_letters(string: str) -> str:
    """
    Function to remove everything but alphabet
    letters from a given string

    :param string: string
    :return: cleaned string
    """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")

    letters_only = [symbol for symbol in string if symbol in LETTERS_AND_SPACE]

    return ''.join(letters_only)
