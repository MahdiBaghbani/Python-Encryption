from collections import defaultdict

from lib.Characters import LETTERS, ETAOIN, ETAOIN_ALL

englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
                     'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23,
                     'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
                     'Q': 0.10, 'Z': 0.07}


def get_letter_count(string: str) -> dict:
    """ Function that counts every symbol in a string """
    # a dictionary to save symbol count
    letter_count = defaultdict(int)

    for letter in string:
        if letter in LETTERS:
            letter_count[letter] += 1

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
        if uncommonLetter in freq_order[: -8: -1]:
            match_score += 1

    return match_score
