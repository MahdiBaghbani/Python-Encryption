import argparse

import io_library
from Characters import CHARACTERS


def main():
    parser = argparse.ArgumentParser(description='This is Shift Cipher module')
    parser.add_argument('-i', '--input', help='Input file name')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    parser.add_argument('-k', '--key', type=int, help='Key for encryption', required=True)
    parser.add_argument('-d', '--decrypt', action='store_true', default=False, help='Decryption switch')
    args = parser.parse_args()
    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = shift(x, args.key, args.decrypt)
        io_library.writer(args.output, y, 't')
    elif args.text:
        print(shift(args.text, args.key, args.decrypt))


def shift(text, key, decrypt=False):
    key_size = len(CHARACTERS)

    def enc(char):
        return CHARACTERS[(CHARACTERS.index(char) + key) % key_size]

    def dec(char):
        return CHARACTERS[(CHARACTERS.index(char) - key) % key_size]

    translated = ''
    if decrypt:
        for i in text:
            if i in CHARACTERS:
                i = dec(i)
            translated += i
    else:
        for i in text:
            if i in CHARACTERS:
                i = enc(i)
            translated += i

    return translated


if __name__ == '__main__':
    main()
