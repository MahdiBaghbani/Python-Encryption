import argparse
from sources.io_library import reader, writer


def main():
    parser = argparse.ArgumentParser(description='This is Reverse Cipher module')
    parser.add_argument('-i', '--input', help='Input file name')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    args = parser.parse_args()
    if args.input and args.output:
        x = reader(args.input, 't')
        y = reverse(x)
        writer(args.output, y, 't')
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
