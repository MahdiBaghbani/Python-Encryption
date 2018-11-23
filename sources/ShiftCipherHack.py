import argparse

import ShiftCipher
from lib import FrequencyAnalyzer
from lib import TrueTextDetector
from lib import WordPatternAnalyzer
from lib import io_library
from lib.Characters import LETTERS
from lib.FrequencyAnalyzer import ETAOIN

failed = "FAILED TO HACK CIPHER\n"


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Shift Cipher Hack module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-l', '--letters', type=str, help='letter sequence', default=LETTERS)
    parser.add_argument('-d', '--dictionary', type=str, help='dictionary Path',
                        default=r"dictionaries/english.txt")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Show hacking process')
    parser.add_argument('-s', '--seed', type=int, help='Specify random seed for shuffling letter sequence', default=0)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--bruteForce', action='store_true', help='Brute-Force technique')
    group.add_argument('-f', '--frequencyAnalyzer', action='store_true', help='Frequency analyzing technique')
    args = parser.parse_args()

    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = shift_hack(x, args.letters, args.seed, args.dictionary, args.bruteForce, args.frequencyAnalyzer,
                       args.verbose)
        io_library.writer(args.output, y, 't')

    elif args.text:
        print(shift_hack(args.text, args.letters, args.seed, args.dictionary, args.bruteForce, args.frequencyAnalyzer,
                         args.verbose))

    else:
        raise ValueError("You have to define arguments [-i -o] or -t\n")


def shift_hack(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, bruteforce: bool = True,
               frequency_analyzer: bool = False, verbose: bool = False) -> str:
    """ Function to handle hack procedure"""

    if bruteforce:
        # maximum seed for bruteforce
        if seed:
            for i in range(seed):
                # show output
                if verbose:
                    print("seed => {}".format(i))
                # bruteforce
                plain_text = brute_force(cipher_text, letter_sequence, i, dictionary_path, False, verbose)
                # return hacked text
                if plain_text != failed:
                    return plain_text
            # nothing found
            return failed
        else:
            # bruteforce
            return brute_force(cipher_text, letter_sequence, seed, dictionary_path, True, verbose)

    elif frequency_analyzer:
        cipher_text = analyze(cipher_text)
        return cipher_text


def brute_force(cipher_text: str, letter_sequence: str, seed: int, dictionary_path: str, no_shuffle: bool,
                verbose: bool = False) -> str:
    """ Function to bruteforce shift cipher"""
    # loads dictionary into true text detector module
    words = TrueTextDetector.load_dictionary(dictionary_path)

    # trying every possible key in key space [key space = length letter sequence]
    for i in range(len(letter_sequence)):
        probable_plain_text = ShiftCipher.shift(cipher_text, i, letter_sequence, seed, no_shuffle, True)
        # show output
        if verbose:
            print("key #{}:\n{}\n\n".format(i, probable_plain_text))
        # check if it's correct
        if TrueTextDetector.is_true_text(probable_plain_text, words):
            return probable_plain_text

    return failed


def analyze(cipher_text):
    # words = TrueTextDetector.load_dictionary(r'lib/dictionary_en.txt')
    frequency = FrequencyAnalyzer.get_frequency_order(cipher_text)
    cipher_text = cipher_text.replace(frequency[0], ETAOIN[0])
    """comb = frequency[1:7]
    comb = combination(comb)
    plain = ''
    for seq in comb:
        temp = cipher_text
        for i in range(6):
            temp = temp.replace(seq[i], ETAOIN[i+1])
        if TrueTextDetector.is_true_text(temp, words, 2, 2):
            plain += temp + '\n\n\n\n\n'"""

    return str(WordPatternAnalyzer.hack_simple_sub(cipher_text))


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


if __name__ == '__main__':
    main()
