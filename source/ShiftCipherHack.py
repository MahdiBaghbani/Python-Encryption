import argparse
from collections import defaultdict

import ShiftCipher
from lib import FrequencyAnalyzer
from lib import TrueTextDetector
from lib import WordPatternAnalyzer
from lib import io_library
from lib.Characters import LETTERS, NEW_LINE
from lib.FrequencyAnalyzer import ETAOIN

failed = "FAILED TO HACK CIPHER\n"


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Shift Cipher Hack module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-l', '--letters', type=str, default=LETTERS, help='letter sequence')
    parser.add_argument('-d', '--dictionary', type=str, default=r"dictionaries/english all words.json",
                        help='dictionary Path')
    parser.add_argument('-pd', '--pattern_dictionary', type=str, default=r"patterns/english.json",
                        help='Pattern dictionary path')
    parser.add_argument('-ml', '--max_lines', type=int, default=100, help='Maximum lines to be read')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Show hacking process')
    parser.add_argument('-sk', '--show_key', action='store_true', default=False,
                        help='Show seed and key of hacked text')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='Specify maximum range of  seed for shuffling letter sequence')
    parser.add_argument('-sh', '--shuffle', action='store_true', default=False, help='Shuffle letter sequence')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--bruteForce', action='store_true', help='Brute-Force technique')
    group.add_argument('-f', '--frequencyAnalyzer', action='store_true', help='Frequency analyzing technique')
    args = parser.parse_args()

    if args.input and args.output:
        inputed = io_library.reader(args.input, 't', args.max_lines)
        outputed = shift_hack(inputed, args.letters, args.seed, args.dictionary, args.pattern_dictionary, args.shuffle,
                              args.bruteForce, args.frequencyAnalyzer, args.verbose, args.show_key)
        io_library.writer(args.output, outputed, 't')

    elif args.text:
        print(shift_hack(args.text, args.letters, args.seed, args.dictionary, args.pattern_dictionary, args.shuffle,
                         args.bruteForce, args.frequencyAnalyzer, args.verbose, args.show_key))

    else:
        raise ValueError("You have to define arguments [-i -o] or -t\n")


def shift_hack(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, pattern_dictionary_path: str,
               shuffle: bool = False, bruteforce: bool = True, frequency_analyzer: bool = False, verbose: bool = False,
               show_key: bool = False):
    """ Function to handle hack procedure"""

    if bruteforce:
        # maximum seed for bruteforce
        if seed:
            for i in range(seed):
                # show output
                if verbose:
                    print("Seed => {}\n".format(i))
                # bruteforce
                plain_text = brute_force(cipher_text, letter_sequence, i, dictionary_path, shuffle=True,
                                         verbose=verbose, show_key=show_key)
                # return hacked text
                if plain_text != failed:
                    return plain_text
            # nothing found
            return failed
        else:
            # bruteforce
            return brute_force(cipher_text, letter_sequence, seed, dictionary_path, shuffle, verbose, show_key)

    elif frequency_analyzer:
        return analyze(cipher_text, dictionary_path, pattern_dictionary_path)
        # return cipher_text


def brute_force(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, shuffle: bool,
                verbose: bool, show_key: bool) -> str:
    """ Function to bruteforce shift cipher"""
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

    return failed


def analyze(cipher_text: str, dictionary_path: str, pattern_dictionary_path: str):
    # words = TrueTextDetector.load_dictionary(dictionary_path)
    # get frequency order of cipher_text
    frequency = FrequencyAnalyzer.get_letter_frequency_order(cipher_text)
    # replace the most frequent with ' ' [space], because in 99% of cases
    # the most frequent character in a cipher_text in ' '
    cipher_text = cipher_text.replace(frequency[0], ETAOIN[0])
    # gets potential cipher to letter mapping
    pattern_dictionary = io_library.reader(pattern_dictionary_path, 'j')
    pattern = WordPatternAnalyzer.pattern_mapper(cipher_text, pattern_dictionary)
    # print(pattern)

    """comb = frequency[1:7]
    comb = combination(comb)
    plain = ''
    for seq in comb:
        temp = cipher_text
        for i in range(6):
            temp = temp.replace(seq[i], ETAOIN[i+1])
        if TrueTextDetector.is_true_text(temp, words, 2, 2):
            plain += temp + '\n\n\n\n\n'"""

    # return str(WordPatternAnalyzer.hack_simple_sub(cipher_text))
    return pattern


def index_mapper(string: str):
    """
     Function to create a dictionary that maps every letter
     to a list of indexes of its occurrence in a given
     """
    # adding new line character '\n' tp letters
    letters = LETTERS + NEW_LINE
    # a default dictionary containing the list as key
    index = defaultdict(list)
    for letter in letters:
        index[letter] = find(string, letter)
    return index


def find(string: str, character: str) -> list:
    """
    Function to return index of every occurrence of a given character in a string
    :param string: input string
    :param character: character
    :return: list containing index
    """
    return [i for i, ltr in enumerate(string) if ltr == character]


def combination(string):
    x = len(string)
    ls = list()
    heap_permute(string, x, ls)
    return ls


def heap_permute(string, x, ls: list):
    if x == 1:
        ls.append(string)
    else:
        for i in range(x):
            heap_permute(string, x - 1, ls)
            if x % 2 == 0:
                string = swap(string, 0, x - 1)
            else:
                string = swap(string, i, x - 1)


def swap(target, first: int, second: int, string: bool = True):
    def action():
        temp = target[first]
        target[first] = target[second]
        target[second] = temp
        return target

    if string:
        target = list(target)
        target = action()
        return ''.join(target)
    else:
        return action()


# if __name__ == '__main__':
#     main()

shift_hack(io_library.reader('1.txt', 't'), LETTERS, 0, 'dictionaries/english all words.json', 'patterns/english.json',
           bruteforce=False, frequency_analyzer=True)
