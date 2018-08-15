import argparse

from lib import io_library


def main():
    parser = argparse.ArgumentParser(description='This is Reverse Cipher module')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    args = parser.parse_args()
    if args.input and args.output:
        x = io_library.reader(args.input, 't')
        y = reverse(x)
        io_library.writer(args.output, y, 't')
    elif args.text:
        print(reverse(args.text))


def reverse(text):
    translated = ''
    i = len(text) - 1
    while i >= 0:
        translated = translated + text[i]
        i = i - 1
    return translated


if __name__ == '__main__':
    main()
