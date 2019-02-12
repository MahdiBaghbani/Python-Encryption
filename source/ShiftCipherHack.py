import argparse

import ShiftCipher
from lib import FrequencyAnalyzer
from lib import TextAnalyzer
from lib import TrueTextDetector
from lib import io_library
from lib.Characters import LETTERS

# define global CONSTANT variables [why I'm using global variable? idk!]
FAILED = 0


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Shift Cipher Hack module')

    # input options [Required]
    input_mode = parser.add_mutually_exclusive_group(required=True)
    input_mode.add_argument('-i', '--input', help='Input file path')
    input_mode.add_argument('-t', '--text', help='Text to be hacked')

    # output option
    parser.add_argument('-o', '--output', help='Output file path')

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

    # hacking settings
    parser.add_argument('-ml', '--max_lines', type=int, default=100, help='Maximum lines to be read')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Show hacking process')
    parser.add_argument('-sk', '--show_key', action='store_true', default=False,
                        help='Show seed and key of hacked text')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='Specify maximum range of  seed for shuffling letter sequence')
    parser.add_argument('-sh', '--shuffle', action='store_true', default=False, help='Shuffle letter sequence')
    hack_mode = parser.add_mutually_exclusive_group(required=True)

    # type of decryption
    hack_mode.add_argument('-bf', '--bruteForce', action='store_true', help='Brute-Force technique')
    hack_mode.add_argument('-fa', '--frequencyAnalyzer', action='store_true', help='Frequency analyzing technique')
    args = parser.parse_args()

    # load input with respect to user selected mode
    if args.input:
        input_text = io_library.reader(args.input, 't', args.max_lines)
    else:
        input_text = args.text

    # do hacking process and get an output
    output_text = shift_hack(input_text, args.letters, args.seed, args.dictionary, args.pattern_dictionary,
                             args.frequent_unordered_word_dict, args.shuffle, args.bruteForce,
                             args.frequencyAnalyzer, args.verbose, args.show_key)

    # show user the result
    if args.show_key:
        if output_text[0] == FAILED:
            print("Failed to hack Cipher")
            exit(1)
        else:
            if args.output:
                io_library.writer(args.output, output_text[0], 't')
                io_library.writer(args.output + '_KEY.txt', output_text[1], 't')
            else:
                print(output_text[0], end='\n\n')

            print(output_text[1])
    else:
        if output_text == FAILED:
            print("Failed to hack Cipher")
            exit(1)
        if args.output:
            io_library.writer(args.output, output_text, 't')
        else:
            print(output_text)


def shift_hack(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, pattern_dictionary_path: str,
               frequent_unordered_words_path: str, shuffle: bool = False, bruteforce: bool = True,
               frequency_analyzer: bool = False, verbose: bool = False, show_key: bool = False):
    """
    Function to handle hack procedure

    :param cipher_text: well it's what we are trying to hack
    :param letter_sequence: letter sequence to be used for hacking
    :param seed: maximum seeds to be used in brute-force method
    :param dictionary_path: path to words dictionary file [must be json]
    :param pattern_dictionary_path: path to pattern dictionary file [must be json]
    :param frequent_unordered_words_path: path to frequent unordered words dictionary file [must be json]
    :param shuffle: use shuffled letter sequence in brute-force method
    :param bruteforce: use brute-force method
    :param frequency_analyzer: use frequency analysis method
    :param verbose: show hacking process
    :param show_key: show key after successfully hacking cipher via brute-force method
    """

    # switch between methods
    if bruteforce:
        # maximum seed for bruteforce
        if seed:
            for i in range(seed):
                # show output
                if verbose:
                    print("Seed => {}\n".format(i))
                # brute-force
                plain_set = brute_force(cipher_text, letter_sequence, i, dictionary_path, shuffle=True,
                                        verbose=verbose, show_key=show_key)
                # return plain_set if it's not FAILED
                if show_key and plain_set[0] != FAILED:
                    return plain_set
                elif not show_key and plain_set != FAILED:
                    return plain_set
            # nothing found
            return FAILED
        else:
            # brute-force
            return brute_force(cipher_text, letter_sequence, seed, dictionary_path, shuffle, verbose, show_key)

    elif frequency_analyzer:
        return analyze(cipher_text, dictionary_path, pattern_dictionary_path, frequent_unordered_words_path)
        # return cipher_text


def brute_force(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, shuffle: bool = False,
                verbose: bool = False, show_key: bool = False):
    """
    Function to brute-force shift cipher

    :param cipher_text: what a helpful doc!
    :param letter_sequence: letter sequence to be used for hacking
    :param seed: maximum seeds to be used
    :param dictionary_path: path to words dictionary file [must be json]
    :param shuffle: use shuffled letter sequence
    :param verbose: show hacking process
    :param show_key: show key after successfully hacking cipher via brute-force method
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
            # show hacked key and also return key information
            if show_key:
                key_set = "Seed: {}\nKey: {}\nShuffle: {}\nLetter sequence: {}".format(seed, i, shuffle,
                                                                                       letter_sequence)
                return probable_plain_text, key_set
            # return plain-text
            return probable_plain_text
    # failed to hack cipher-text
    return FAILED


def analyze(cipher_text: str, dictionary_path: str, pattern_dictionary_path: str, frequent_unordered_words_path: str) \
        -> str:
    """
    Seems like this function is only loading neccessary resources for the analyzer_process function

    :param cipher_text: isn't it enough describing?
    :param dictionary_path: path to words dictionary file [must be json]
    :param pattern_dictionary_path: path to pattern dictionary file [must be json]
    :param frequent_unordered_words_path: path to frequent unordered words dictionary file [must be json]
    :return: plain-text string
    """

    # load pattern dictionary
    pattern_dictionary = io_library.reader(pattern_dictionary_path, 'j')
    # load frequent words dictionary
    frequent_words = io_library.reader(frequent_unordered_words_path, 'j')
    # load English words dictionary
    words = TrueTextDetector.load_dictionary(dictionary_path)
    # process the string
    return analyzer_process(cipher_text, pattern_dictionary, frequent_words, words)


def analyzer_process(string: str, pattern_dictionary: dict, frequent_unordered_words_dict: dict, words: set) -> str:
    """
    Reconstructs a plain-text by using a letter_map dictionary of the cipher-text

    :param string: cipher-text to be decrypted
    :param pattern_dictionary: decrypt letter letter_map
    :param frequent_unordered_words_dict: a dictionary of frequent unordered words
    :param words: set of word for TrueTextDetector module
    :return: plain-text string
    """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string")

    # get cipher_letter_frequency of letters in string
    cipher_letter_frequency = FrequencyAnalyzer.get_letter_frequency_order(string)

    # the most frequent letter in a cipher-text is always mapped to space (' ') in plain-text <"ASSUMPTION">
    space = cipher_letter_frequency[0]

    # get letter_index_map dictionary of letters in cipher text,
    # this must be done before replacing most frequent letter with space!
    letter_index_map = TextAnalyzer.index_mapper(string, 'letter', cipher_letter_frequency)

    # get letter_map of words in the string
    letter_map = TextAnalyzer.pattern_mapper(string, pattern_dictionary, space, cipher_letter_frequency)

    # replace the cipher-letter mapped to space with space, this must be done after letter_map analysis,
    # to avoid analysis jamming
    string = string.replace(space, ' ')

    # create an output based on letter_map and letter_index_map
    output_string = TextAnalyzer.string_filler(letter_map, letter_index_map, string_length=len(string))

    # test high cipher_letter_frequency letters and repair them if their mapped plain-letter are wrong
    repaired_map_dict = TextAnalyzer.test_high_frequency(string, ''.join(output_string), letter_map, letter_index_map,
                                                         cipher_letter_frequency, frequent_unordered_words_dict, words)

    # repair letter_map with repaired_map_dict
    letter_map = TextAnalyzer.repair_mapping(letter_map, repaired_map_dict, cipher_letter_frequency)

    # refill the out_put string based on newly repaired letter_map and same letter_index_map as before
    output_string = TextAnalyzer.string_filler(letter_map, letter_index_map, string=output_string)

    # replace every 10th space with newline
    for i, j in enumerate(letter_index_map[space]):
        if i % 10 == 0 and i != 0:
            output_string[j] = '\n'

    # return plain-text string return ''.join(output_string)
    return ''.join(output_string)


# execute program in terminal
if __name__ == '__main__':
    main()
