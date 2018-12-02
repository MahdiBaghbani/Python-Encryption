import operator
from collections import defaultdict, namedtuple

from lib.Characters import LETTERS, ETAOIN, ETAOIN_ALL


def get_word_frequency_order(string: str, length: str) -> tuple:
    word_list = string.split()

    if length == '1' or 'all':
        one = get_word_order(word_list, 1)
    if length == '2' or 'all':
        two = get_word_order(word_list, 2)
    if length == '3' or 'all':
        three = get_word_order(word_list, 3)
    if length == '4' or 'all':
        four = get_word_order(word_list, 4)

    if length == 'all':
        frequency_order = namedtuple('frequency_order', 'one two three four')
        return frequency_order(one, two, three, four)

    elif length == '1':
        return one
    elif length == '2':
        return two
    elif length == '3':
        return three
    elif length == '4':
        return four
    else:
        raise ValueError("length argument is not valid!\n")


def get_word_order(word_list: list, length) -> tuple:
    dictionary = defaultdict(int)
    for i in word_list:
        if len(i) == length:
            dictionary[i] += 1
    dictionary.default_factory = None
    dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return tuple([i[0] for i in dictionary])


def alphabetical_sort(dataset: list, reverse=False, dictionary=None):
    if not dictionary:
        dictionary = defaultdict(list)
    for item in dataset:
        if reverse:
            dictionary[item[-1]].append(item)
        else:
            dictionary[item[0]].append(item)
    return dictionary


def english_freq_match_score(string: str) -> tuple:
    """
    Function to calculate frequency score of
    a given string according to English frequency
    """

    freq_order = get_letter_frequency_order(string)
    freq_order = freq_order.upper()
    match_score = 0
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
