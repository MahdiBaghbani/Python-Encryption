import argparse
import random
from lib import io_library
from lib.Characters import LETTERS


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Shift Cipher module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-k', '--key', type=int, help='Key for encryption', required=True)
    parser.add_argument('-l', '--letters', type=str, help='letters sequence', default=LETTERS)
    parser.add_argument('-d', '--decrypt', action='store_true', default=False, help='Decryption switch')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--seed', type=int, help='Specify random seed for shuffling letter sequence', default=0)
    group.add_argument('-ns', '--noShuffle', help='Don\'t shuffle letter sequence', action='store_false', default=True)
    args = parser.parse_args()

    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = shift(x, args.key, args.letters, args.seed, args.noShuffle, args.decrypt)
        io_library.writer(args.output, y, 't')
    elif args.text:
        print(shift(args.text, args.key, args.letters, args.seed, args.noShuffle, args.decrypt))
    else:
        raise ValueError("You have to define arguments [-i -o] or -t\n")


class Shift:
    """ Shift cipher class """

    def __init__(self, key: int, letter_sequence: str = LETTERS, seed: int = 0, shuffle: bool = True):
        self.key = key
        self.seed = seed
        self.shuffle = shuffle
        self.letter_sequence = letter_sequence

    def encrypt(self, text: str):
        return shift(text, self.key, self.letter_sequence, self.seed, self.shuffle)

    def decrypt(self, text: str):
        return shift(text, self.key, self.letter_sequence, self.seed, self.shuffle, True)

    def config(self, key: int = None, letter_sequence: str = None, seed: int = None, shuffle: bool = None):
        if key:
            self.key = key
        if seed:
            self.seed = seed
        if shuffle:
            self.shuffle = shuffle
        if letter_sequence:
            self.letter_sequence = letter_sequence


def shift(text: str, key: int, letter_sequence: str, seed: int, shuffle: bool, decrypt: bool = False) -> str:
    """
        Function to shift letters
        :param text : text to be shifted
        :param key: key for shifting
        :param letter_sequence: the letter sequence the will be shifted with respect of the key
        :param seed: randomizes the letter sequence by shuffling it
        :param shuffle: flag for using shuffle
        :param decrypt: reverse the key to decrypt
        :return shifted text
    """

    key_size = len(letter_sequence)  # this is our key space

    if shuffle:  # self explaining
        letter_sequence = letter_shuffle(letter_sequence, seed)

    translated = ''  # new string variable to hold translated text

    if decrypt:  # reverse key for decryption
        key *= -1

    for char in text:
        if char in letter_sequence:
            # in this section we add the key to char's index number and then calculate it's modulo with respect to
            # our key space, the result number will be the index of new mapped char to our original char
            char = letter_sequence[(letter_sequence.index(char) + key) % key_size]

        translated += char  # add mapped char to string variable

    return translated


def letter_shuffle(letter_str: str, s: int) -> str:
    """
    Function to shuffle a word sequence
    :param letter_str:
    :param s:
    :return: word sequence
    """
    random.seed(s)
    letter_list = list(letter_str)
    random.shuffle(letter_list)
    return ''.join(letter_list)


if __name__ == '__main__':
    main()
