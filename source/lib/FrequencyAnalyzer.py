import operator
from collections import defaultdict

from lib.Characters import LETTERS, ETAOIN, ETAOIN_ALL


def get_word_frequency_order(string: str, length: str) -> list:
    word_list = string.split()
    frequency_order = [[], [], [], []]
    if length == '1' or 'all':
        frequency_order[0] = get_word_order(word_list, 1)
    if length == '2' or 'all':
        frequency_order[1] = get_word_order(word_list, 2)
    if length == '3' or 'all':
        frequency_order[2] = get_word_order(word_list, 3)
    if length == '4' or 'all':
        frequency_order[3] = get_word_order(word_list, 4)

    return frequency_order


def get_word_order(word_list: list, length) -> tuple:
    dictionary = defaultdict(int)
    for i in word_list:
        if len(i) == length:
            dictionary[i] += 1
    dictionary.default_factory = None
    dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return tuple([i[0] for i in dictionary])


def alphabetical_sort(dataset: list, dictionary: bool = None, reverse: bool = False, both: bool = False):

    if not dictionary:
        dictionary = defaultdict(set)

    for item in dataset:
        if both:
            dictionary[item[-1]].add(item)
            dictionary[item[0]].add(item)
        else:
            if reverse:
                dictionary[item[-1]].add(item)
            else:
                dictionary[item[0]].add(item)

    return dictionary


def english_freq_match_score(string: str) -> tuple:
    """
    Function to calculate frequency score of
    a given string according to English frequency
    """
    # get the frequency order of a given string
    freq_order = get_letter_frequency_order(string)
    # uppercase all letters
    freq_order = freq_order.upper()
    # start score from 0
    match_score = 0
    # for common letters in first 6 letters of the string frequency
    #  and English frequency add 1 to score
    for commonLetter in ETAOIN[:7]:
        if commonLetter in freq_order[: 7]:
            match_score += 1

    return match_score, freq_order


def get_letter_frequency_order(string: str) -> str:
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


def get_letter_count(string: str) -> dict:
    """ Function that counts every symbol in a string """
    # a dictionary to save symbol count
    letter_count = defaultdict(int)

    for letter in string:
        if letter in LETTERS:
            letter_count[letter] += 1

    letter_count.default_factory = None

    return letter_count


def get_item_at_index_zero(x):
    return x[0]
