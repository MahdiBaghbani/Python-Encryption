import argparse
import random
from lib import io_library
from lib.Characters import LETTERS


def main():
    parser = argparse.ArgumentParser(description='This is Shift Cipher module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-k', '--key', type=int, help='Key for encryption', required=True)
    parser.add_argument('-l', '--letters', type=str, help='letters sequence', default=LETTERS)
    parser.add_argument('-d', '--decrypt', action='store_true', default=False, help='Decryption switch')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--seed', type=int, help='Specify random seed for shuffling letter sequence', default=0)
    group.add_argument('-ns', '--noShuffle', help='Don\'t shuffle letter sequence', action='store_true', default=False)
    args = parser.parse_args()
    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = shift(x, args.key, args.letters, args.seed, args.noShuffle, args.decrypt)
        io_library.writer(args.output, y, 't')
    elif args.text:
        print(shift(args.text, args.key, args.letters, args.seed, args.noShuffle, args.decrypt))


def shift(text: str, key: int, letter_sequence: str, seed: int, no_shuffle: bool = False, decrypt: bool = False) -> str:
    key_size = len(letter_sequence)
    if not no_shuffle:
        letter_sequence = letter_shuffle(letter_sequence, seed)
    translated = ''
    if decrypt:
        key *= -1
    for char in text:
        if char in letter_sequence:
            char = letter_sequence[(letter_sequence.index(char) + key) % key_size]
        translated += char

    return translated


def letter_shuffle(letter_str: str, s: int) -> str:
    random.seed(s)
    letter_list = list(letter_str)
    random.shuffle(letter_list)
    return ''.join(letter_list)


if __name__ == '__main__':
    main()
