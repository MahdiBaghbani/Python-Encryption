import operator
from collections import defaultdict

from lib.Characters import ETAOIN, ETAOIN_ALL


def get_word_frequency_order(string: str, length: str) -> dict:
    """
    This function will return a dictionary containing a list most frequent words by length

    :param string: string text to be analyzed
    :param length: desired length
    :return: dictionary with length as keys and values a list containing words ordered by their frequency
    """
    # check inputs
    if not (type(string) == str and type(length) == str):
        raise TypeError("Arguments 'string' and 'length' of this function must be of type string.\n")

    # split string into words
    word_list = string.split()
    # create output dictionary
    frequency_order = defaultdict(list)

    # get frequency order of words with lengths 1 to 4
    if length == 'all':
        for i in range(1, 5):
            frequency_order[str(i)] = get_word_order(word_list, i)
    # get frequency of arbitrary length of words
    else:
        # convert length from string to integer
        try:
            int_length = int(length)
        except ValueError:
            raise ValueError("Length argument must be an integer in type of string! example: '3'.\n")
        else:
            frequency_order[length] = get_word_order(word_list, int_length)
    # convert default dictionary to dictionary and return it
    return dict(frequency_order)


def get_word_order(word_list: list, length: int) -> list:
    """
    This function will return a frequency ordered list of words with specific length

    :param word_list: list of words
    :param length: length of target words
    :return: frequency ordered list of words with specific length
    """

    # check inputs
    if not type(word_list) == list:
        raise TypeError("Argument 'word_list' of this function must be of type list.\n")
    if not type(length) == int:
        raise TypeError("Argument 'length' of this function must be of type integer.\n")

    # create a default dict with values of type int
    dictionary = defaultdict(int)
    # for word in word_list if the words length is the one we are searching for,
    # add the word as key to dictionary and add 1 to in's value as counter
    for i in word_list:
        if len(i) == length:
            dictionary[i] += 1
    # convert default dict to dict
    dictionary = dict(dictionary)
    # sort all words in dictionary based on their counters, reverse true means
    # the words with higher counter numbers will be at start of list
    dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    # return frequency ordered words in a list
    return [get_item_at_index_zero(i) for i in dictionary]


def alphabetical_sort(word_list: list, dictionary: defaultdict = None, reverse: bool = False, both: bool = False) \
        -> defaultdict:
    """
    This function will return a default dict that has keys
    of first or last letter of words and values with sets
    of words corresponding to the keys, it can also take
    an already created dictionary instead of creating a blank one

    :param word_list: list of words
    :param dictionary: if a dictionary already exists,
    use it instead of blank dictionary, defaultdict must has 'set' as default value
    :param reverse: sort based on last letter of words
    :param both: sort based on both first and last letters of words
    :return: a default dictionary
    """

    # check inputs
    if not type(word_list) == list:
        raise TypeError("Argument 'word_list' of this function must be of type list.\n")
    if not type(dictionary) == defaultdict:
        raise TypeError("Argument 'dictionary' of this function must be of type defaultdict.\n")
    if not (type(reverse) == bool and type(both) == bool):
        raise TypeError("Arguments 'reverse' and 'both' of this function must be of type boolean.\n")

    # create a blank default dict if no dictionary is provided by input
    if not dictionary:
        dictionary = defaultdict(set)

    for item in word_list:
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

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")

    # get the frequency order of a given string
    freq_order = get_letter_frequency_order(string)
    # uppercase all letters
    freq_order = freq_order.upper()
    # start score from 0
    match_score = 0
    # for common letters in first 6 letters of the string frequency
    #  and English frequency add 1 to score
    for commonLetter in ETAOIN[:7]:
        if commonLetter in freq_order[:7]:
            match_score += 1

    return match_score, freq_order


def get_letter_frequency_order(string: str) -> str:
    """ Function to create frequency order of a given string """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")

    # count every symbol in string
    letter_count = get_letter_count(string)

    # create a dictionary which maps number of occurrences
    #  to a list of symbols
    frequency = defaultdict(list)
    for i in letter_count:
        frequency[letter_count[i]].append(i)

    # convert default dict to dict
    frequency = dict(frequency)

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

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")

    # a dictionary to save symbol count
    letter_count = defaultdict(int)

    for letter in string:
        letter_count[letter] += 1

    return dict(letter_count)


def get_item_at_index_zero(x):
    """ Returns item at index zero """
    return x[0]
