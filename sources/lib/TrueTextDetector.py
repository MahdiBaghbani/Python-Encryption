import argparse
from lib import io_library
from lib.Characters import LETTERS_AND_SPACE


def main():
    """ Function to run program from Terminal
    """
    parser = argparse.ArgumentParser(description='This is True Text Detector module')
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('-i', '--input', help='Input file path')
    source.add_argument('-t', '--text', help='Text to be analyzed')
    parser.add_argument('-d', '--dictionary', type=str, help='Dictionary file path ', required=True)
    parser.add_argument('-w', '--word', type=int, default=20, help='Word percentage threshold')
    parser.add_argument('-l', '--letter', type=int, default=85, help='Letter percentage threshold')
    args = parser.parse_args()
    word_set = load_dictionary(args.dictionary)
    if args.input:
        message = io_library.reader(args.input, 't')
    elif args.text:
        message = args.text
    if is_true_text(message, word_set, args.word, args.letter):
        print('True')
    else:
        print("False")


def is_true_text(message: str, words: set, word_percentage: int = 20, letter_percentage: int = 85) -> bool:
    """ Function to determine if the given string is proper text or not
    you can adjust sensitivity and overwrite default threshold percentage

    :param message: string to be examined
    :param words: set of words
    :param word_percentage: minimum words threshold
    :param letter_percentage: minimum letter in string threshold
    :rtype: bool
    """
    words_match = get_words_count(message, words) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message))
    message_letters_percentage = num_letters / len(message) * 100
    letters_match = message_letters_percentage >= letter_percentage

    return words_match and letters_match


def load_dictionary(file: str) -> set:
    """ Function to load dictionary file's words into a set

    :param file: path to dictionary file
    :return: set of dictionary words
    :rtype: set
    """
    dictionary = io_library.reader(file, 't').split('\n')
    words = set()
    for word in dictionary:
        words.add(word)

    return words


def remove_non_letters(message: str):
    """ Function to remove everything but alphabet
     letters from a given string

    :param message: string
    :return: cleaned string
    """
    letters_only = list()
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            letters_only.append(symbol)

    return ''.join(letters_only)


def get_words_count(message: str, words: set):
    """ Function to count matches between words in
     a string and a dictionary set

    :param message: string to be examined
    :param words: dictionary set
    :return: ratio matches/all words
    """
    message = message.upper()
    message = remove_non_letters(message)
    possible_words = message.split()
    if not possible_words:
        return 0.0
    matches = 0
    for word in possible_words:
        if word in words:
            matches += 1

    return matches / len(possible_words)


if __name__ == '__main__':
    main()
