import argparse

import ShiftCipher
from lib import io_library
from lib import TrueTextDetector
from lib import FrequencyAnalyzer
from lib.FrequencyAnalyzer import ETAOIN
from lib.Characters import LETTERS

failed = "FAILED TO HACK CIPHER\n"

def main():
    parser = argparse.ArgumentParser(description='This is Shift Cipher Hack module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-l', '--letters', type=str, help='letters sequence', default=LETTERS)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Show hacking process')
    parser.add_argument('-s', '--seed', type=int, help='Specify random seed for shuffling letter sequence')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--bruteForce', action='store_true', help='Brute-Force technique')
    group.add_argument('-f', '--frequencyAnalyzer', action='store_true', help='Frequency analyzing technique')
    args = parser.parse_args()
    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = shift_hack(x, args.letters, args.seed, args.bruteForce, args.frequencyAnalyzer, args.verbose)
        io_library.writer(args.output, y, 't')
    elif args.text:
        print(shift_hack(args.text, args.letters, args.seed, args.bruteForce, args.frequencyAnalyzer, args.verbose))
    else:
        raise ValueError("you have to define arguments [-i -o] or -t\n")


def shift_hack(cipher_text: str, letter_sequence: str, seed: int, bruteforce: bool = True, frequency_analyzer: bool = False, verbose: bool = False) -> str:
    if bruteforce:
        if seed:
            for i in range(seed):
                if verbose:
                    print("seed => {}".format(i))
                plain_text = brute_force(cipher_text, letter_sequence, i, False, verbose)
                if plain_text != failed:
                    return plain_text
            return failed
        else:
            return brute_force(cipher_text, letter_sequence, 0, True, verbose)
    elif frequency_analyzer:
        cipher_text = analyze(cipher_text)
        return cipher_text


def analyze(cipher_text):
    words = TrueTextDetector.load_dictionary(r'lib/dictionary_en.txt')
    frequency = FrequencyAnalyzer.get_frequency_order(cipher_text)
    cipher_text = cipher_text.replace(frequency[0], ETAOIN[0])
    comb = frequency[1:7]
    comb = combination(comb)
    plain = ''
    for seq in comb:
        temp = cipher_text
        for i in range(6):
            temp = temp.replace(seq[i], ETAOIN[i+1])
        if TrueTextDetector.is_true_text(temp, words, 2, 2):
            plain += temp + '\n\n\n\n\n'

    return plain


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
            heap_permute(string, x-1, ls)
            if x % 2 == 0:
                string = swap(string, 0, x-1)
            else:
                string = swap(string, i, x-1)


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


def brute_force(cipher_text: str, letter_sequence: str, seed: int, no_shuffle: bool, verbose: bool = False) -> str:
    words = TrueTextDetector.load_dictionary(r'lib/dictionary_en.txt')
    for i in range(len(letter_sequence)):
        probable_plain_text = ShiftCipher.shift(cipher_text, i, letter_sequence, seed, no_shuffle, True)
        if verbose:
            print("key #{}:\n{}\n\n".format(i, probable_plain_text))
        if TrueTextDetector.is_true_text(probable_plain_text, words):
            return probable_plain_text
    return failed


if __name__ == '__main__':
    main()
