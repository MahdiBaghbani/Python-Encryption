import argparse

from lib import io_library


def main():
    """ Wrapper for executing program in terminal """

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
    else:
        raise ValueError("You have to define arguments [-i -o] or -t\n")


def reverse(text: str):
    """
    Function to reverse a text
    :param text: text to be reversed
    :return reversed text
    """
    translated = ''  # new string variable to hold translated text

    i = len(text) - 1
    while i >= 0:
        translated += text[i]
        i -= 1

    return translated


if __name__ == '__main__':
    main()
