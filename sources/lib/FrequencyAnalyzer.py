import argparse
from collections import defaultdict

from lib.Characters import LETTERS, ETAOIN, ETAOIN_ALL
from lib import io_library


def main():
    """ Wrapper for executing program in terminal """

    parser = argparse.ArgumentParser(description='This is Frequency Analyzer program')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--text', help='Text to be encrypted')
    args = parser.parse_args()

    if args.input and args.output:
        text = io_library.reader(args.input, 't')
        print("Calculated score for the input is: {}/14".format(english_freq_match_score(text)))
    elif args.text:
        print("Calculated score for the input is: {}/14".format(english_freq_match_score(args.text)))


def get_letter_count(string: str) -> dict:
    """ Function that counts every symbol in a string """
    # a dictionary to save symbol count
    letter_count = defaultdict(int)

    for letter in string:
        if letter in LETTERS:
            letter_count[letter] += 1

    letter_count.default_factory = None

    return letter_count


def get_frequency_order(string: str) -> str:
    """ Function to create frequency order of a given string """
    # count every symbol in string
    letter_count = get_letter_count(string)

    # create a dictionary which maps number of occurrences
    #  to a list of symbols
    frequency = defaultdict(list)
    for i in letter_count:
        frequency[letter_count[i]].append(i)

    frequency.default_factory = None

    # sort every list in dictionary and replace them by
    #  a string containing items in that list
    for freq in frequency:
        frequency[freq].sort(key=ETAOIN_ALL.find, reverse=True)
        frequency[freq] = ''.join(frequency[freq])

    # get all items in dictionary and sort them from most occurrence
    # to least occurrence
    freq_pairs = list(frequency.items())
    freq_pairs.sort(key=get_item_at_index_zero, reverse=True)

    # create a list and get all symbols in order
    # to create frequency order string
    freq_order = [pair[1] for pair in freq_pairs]

    return ''.join(freq_order)


def get_item_at_index_zero(x):
    return x[0]


def english_freq_match_score(string: str) -> int:
    """
    Function to calculate frequency score of
    a given string according to English frequency
    """

    freq_order = get_frequency_order(string)
    freq_order = freq_order.upper()
    match_score = 0
    for commonLetter in ETAOIN[:7]:
        if commonLetter in freq_order[: 7]:
            match_score += 1
    for uncommonLetter in ETAOIN[-7:]:
        if uncommonLetter in freq_order[-7:]:
            match_score += 1

    return match_score
