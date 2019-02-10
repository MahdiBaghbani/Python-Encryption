import argparse

import ShiftCipher
from lib import FrequencyAnalyzer
from lib import TrueTextDetector
from lib import TextAnalyzer
from lib import io_library
from lib.Characters import LETTERS


# define global CONSTANT variables
FAILED = 0


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Shift Cipher Hack module')
    # input and output options and paths
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    # letter sequence
    parser.add_argument('-l', '--letters', type=str, default=LETTERS, help='letter sequence')
    # dictionaries
    parser.add_argument('-d', '--dictionary', type=str, default=r"dictionaries/english all words.json",
                        help='dictionary Path')
    parser.add_argument('-pd', '--pattern_dictionary', type=str, default=r"patterns/english.json",
                        help='Pattern dictionary path')
    parser.add_argument('-fuwd', '--frequent_unordered_word_dict', type=str,
                        default=r"dictionaries/english words unordered.json",
                        help='english most frequent words dictionary path')
    # decrypt settings
    parser.add_argument('-ml', '--max_lines', type=int, default=100, help='Maximum lines to be read')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Show hacking process')
    parser.add_argument('-sk', '--show_key', action='store_true', default=False,
                        help='Show seed and key of hacked text')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='Specify maximum range of  seed for shuffling letter sequence')
    parser.add_argument('-sh', '--shuffle', action='store_true', default=False, help='Shuffle letter sequence')
    group = parser.add_mutually_exclusive_group(required=True)
    # type of decryption
    group.add_argument('-bf', '--bruteForce', action='store_true', help='Brute-Force technique')
    group.add_argument('-fa', '--frequencyAnalyzer', action='store_true', help='Frequency analyzing technique')
    args = parser.parse_args()

    if args.input and args.output:
        input_text = io_library.reader(args.input, 't', args.max_lines)
        output_text = shift_hack(input_text, args.letters, args.seed, args.dictionary, args.pattern_dictionary,
                                 args.frequent_unordered_word_dict, args.shuffle, args.bruteForce,
                                 args.frequencyAnalyzer, args.verbose, args.show_key)
        io_library.writer(args.output, output_text, 't')

    elif args.text:
        print(shift_hack(args.text, args.letters, args.seed, args.dictionary, args.pattern_dictionary,
                         args.frequent_unordered_word_dict, args.shuffle, args.bruteForce, args.frequencyAnalyzer,
                         args.verbose, args.show_key))

    else:
        raise ValueError("You have to define arguments [-i -o] or -t\n")


def shift_hack(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, pattern_dictionary_path: str,
               frequent_unordered_word_path: str, shuffle: bool = False, bruteforce: bool = True,
               frequency_analyzer: bool = False, verbose: bool = False, show_key: bool = False):
    """
    Function to handle hack procedure

    :param cipher_text:
    :param letter_sequence:
    :param seed:
    :param dictionary_path:
    :param pattern_dictionary_path:
    :param frequent_unordered_word_path:
    :param shuffle:
    :param bruteforce:
    :param frequency_analyzer:
    :param verbose:
    :param show_key:
    :return:
    """

    if bruteforce:
        # maximum seed for bruteforce
        if seed:
            for i in range(seed):
                # show output
                if verbose:
                    print("Seed => {}\n".format(i))
                # brute-force
                plain_text = brute_force(cipher_text, letter_sequence, i, dictionary_path, shuffle=True,
                                         verbose=verbose, show_key=show_key)
                # return hacked text
                if plain_text != FAILED:
                    return plain_text
            # nothing found
            return FAILED
        else:
            # brute-force
            return brute_force(cipher_text, letter_sequence, seed, dictionary_path, shuffle, verbose, show_key)

    elif frequency_analyzer:
        return analyze(cipher_text, dictionary_path, pattern_dictionary_path, frequent_unordered_word_path)
        # return cipher_text


def brute_force(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, shuffle: bool,
                verbose: bool, show_key: bool):
    """
    Function to brute-force shift cipher

    :param cipher_text:
    :param letter_sequence:
    :param seed:
    :param dictionary_path:
    :param shuffle:
    :param verbose:
    :param show_key:
    :return:
    """

    # loads dictionary into true text detector module
    words = TrueTextDetector.load_dictionary(dictionary_path)
    # trying every possible key in key space [key space = length letter sequence]
    for i in range(len(letter_sequence)):
        probable_plain_text = ShiftCipher.shift(cipher_text, i, letter_sequence, seed, shuffle, decrypt=True)
        # show output
        if verbose:
            print("key #{}:\n{}\n\n".format(i, probable_plain_text))
        # check if it's correct
        if TrueTextDetector.is_true_text(probable_plain_text, words):
            # show hacked key
            if show_key:
                print("Seed: {}\nKey: {}\nShuffle: {}\nLetters: {}".format(seed, i, shuffle, letter_sequence))
            return probable_plain_text

    return FAILED


def analyze(cipher_text: str, dictionary_path: str, pattern_dictionary_path: str, frequent_unordered_word_path: str):
    """

    :param cipher_text:
    :param dictionary_path:
    :param pattern_dictionary_path:
    :param frequent_unordered_word_path:
    :return:
    """

    # load pattern dictionary
    pattern_dictionary = io_library.reader(pattern_dictionary_path, 'j')
    # load frequent words dictionary
    frequent_words = io_library.reader(frequent_unordered_word_path, 'j')
    # load English words dictionary
    words = TrueTextDetector.load_dictionary(dictionary_path)
    # process the string
    return analyzer_process(cipher_text, pattern_dictionary, frequent_words, words)


def analyzer_process(string: str, pattern_dictionary: dict, frequent_unordered_word_dict: dict, words: set) -> str:
    """
    Reconstructs a plain-text by using a pattern dictionary of the cipher-text
    :param string: cipher-text to be decrypted
    :param pattern_dictionary: decrypt letter pattern
    :param frequent_unordered_word_dict:
    :param words:
    :return: plain-text string
    """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string")

    # get frequency of letters in string
    frequency = FrequencyAnalyzer.get_letter_frequency_order(string)

    # the most frequent letter in a cipher-text is always mapped to space (' ') in plain-text <"ASSUMPTION">
    space = frequency[0]

    # get index dictionary of letters in cipher text
    index = TextAnalyzer.index_mapper(string, 'letter')

    # replace the cipher-letter mapped to space with space
    string = string.replace(space, ' ')

    # get pattern of words in the string
    pattern = TextAnalyzer.pattern_mapper(string, pattern_dictionary)

    # create a blank text with length equal to cipher-text
    output_string = ['_'] * len(string)

    # replace '_' with space
    for i in index[space]:
        output_string[i] = ' '

    # loop to reconstruct plain-txt from solved cipher-letters
    for letter in pattern.keys():
        # if the cipher-letter "letter" is solved, it's corresponding set must be of size 1
        if letter != space and len(pattern[letter]) == 1:
            # extract plain-letter from set
            plain_letter = next(iter(pattern[letter]))
            # use indexes of cipher-letter "letter" in cipher-text to place plain-letter in correct position
            for i in index[letter]:
                output_string[i] = plain_letter
    # test high frequency letters and repair them if their mapped plain-letter is wrong
    repaired_dict = TextAnalyzer.test_high_frequency(string, ''.join(output_string), pattern, index, frequency[1:7],
                                                     frequent_unordered_word_dict, words)
    # replace repaired letter in plain-text
    for letter in repaired_dict:
        for i in index[letter]:
            output_string[i] = repaired_dict[letter]

    # replace every 10th space with newline
    for i, j in enumerate(index[space]):
        if i % 10 == 0 and i != 0:
            output_string[j] = '\n'

    # return plain-text string return ''.join(output_string)
    return ''.join(output_string)


# execute program in terminal
if __name__ == '__main__':
    main()
