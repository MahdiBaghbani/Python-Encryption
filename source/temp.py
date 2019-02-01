from ShiftCipherHack import shift_hack
from collections import defaultdict
from lib import io_library
from lib.Characters import LETTERS, NEW_LINE, ETAOIN_ALL
from worker import fuck
from lib.WordPatternAnalyzer import blank_mapper_dict, add_letters_to_mapping, intersect_mappings
from lib.WordPatternAnalyzer import remove_solved_letters_from_mapping
from lib.FrequencyAnalyzer import get_letter_frequency_order, get_word_frequency_order


def index_mapper(string: str, mode: str, word=None):
    """
     Function to create a dictionary that maps every letter
     to a list of indexes of its occurrence in a given
     """
    if mode == "letter":
        # adding new line character '\n' tp letters
        letters = LETTERS + NEW_LINE
        # a default dictionary containing the list as key
        index = defaultdict(list)
        for letter in letters:
            index[letter] = letter_index_finder(string, letter)
        return index
    elif mode == "word" and word:
        string = string.split()
        counter = 0
        for i in string:
            if i == word:
                counter += 1
        start_index = 0
        index = 0
        index_list = list()
        for i in range(0, counter):
            end_index = string[start_index : -1].index(word) + start_index + 1
            partial_string = string[start_index : end_index]
            start_index = end_index
            index += word_index_finder(' '.join(partial_string), word)
            index_list.append(index)
        return index_list
    else:
        raise AttributeError("Function mode is wrong.")


def letter_index_finder(string: str, character: str) -> list:
    """
    Function to return index of every occurrence of a given character in a string
    :param string: input string
    :param character: character
    :return: list containing index
    """
    return [i for i, ltr in enumerate(string) if ltr == character]

def word_index_finder(string: str, word: str):
    string_list = string.split()
    index = string_list.index(word)
    counter = 0
    for i in range(0, index):
        counter += len(string_list[i])
    return counter + index

def string_filler(string: str, pattern: dict, string_letter_frequency: str):
    index = index_mapper(string)
    output_string = ['_'] * len(string)

    counter = 1
    for i in index[string_letter_frequency[0]]:
        if counter % 10 != 0:
            output_string[i] = ' '
        else:
            output_string[i] = '\n'
        counter += 1

    #pattern[string_letter_frequency[1]] = {'E'}

    for letter in pattern.keys():
        if len(pattern[letter]) == 1:
            for i in index[letter]:
                output_string[i] = next(iter(pattern[letter]))
        elif len(pattern[letter]) > 1:
            letter_index = string_letter_frequency.index(letter)
            candidate_indexes = [ETAOIN_ALL.index(i) for i in pattern[letter]]
            minimum = min([abs(i - letter_index) for i in candidate_indexes])
            fill = [i for i in candidate_indexes if abs(i - letter_index) == minimum]
            fill.sort()
            for i in index[letter]:
                output_string[i] = ETAOIN_ALL[fill[0]]
    return ''.join(output_string)


def reverse_mapper(pattern: dict) -> dict:
    reverse = blank_mapper_dict()
    for i in pattern.keys():
        if len(pattern[i]) == 1:
            reverse[next(iter(pattern[i]))].add(i)
    return remove_solved_letters_from_mapping(reverse)


def fucker(a):
    b = {"{}".format(len(i)): [j for j in a if len(j) == len(i)] for i in a}
    return b


def key_remover(a, b):
    keys = list(a.keys())
    for i in keys:
        if i not in b:
            del a[i]
    return a


def mapper(map1, map2):
    intersected_map = blank_mapper_dict()
    for word1 in map1:
        new_map = blank_mapper_dict()
        for word2 in map2:
            add_letters_to_mapping(new_map, word1, word2)
        intersected_map = intersect_mappings(intersected_map, new_map)

    return remove_solved_letters_from_mapping(intersected_map)


def frequency_aided_mapper(pattern, target, ordered_source, unordered_source):

    for letter in pattern.keys():

        if len(pattern[letter]) == 1:
            if letter in target:
                probable_letter = next(iter(pattern[letter]))
                if probable_letter in ordered_source and len(ordered_source[probable_letter]) >= len(target[letter]):
                    target_dict = fucker(target[letter])
                    source_dict = unordered_source[probable_letter]
                    source_dict = key_remover(source_dict, target_dict)
                    final_map = blank_mapper_dict()
                    for i in target_dict.keys():
                        try:
                            map = mapper(target_dict[i], source_dict[i])
                            final_map = intersect_mappings(final_map, map)
                        except KeyError:
                            pass
                    pattern = intersect_mappings(pattern, final_map)
                    pattern = remove_solved_letters_from_mapping(pattern)
                else:
                    pattern[letter] = set()
    return pattern


pattern = shift_hack(io_library.reader('1.txt', 't'), LETTERS, 0, 'dictionaries/english all words.json',
                     'patterns/english.json', True, False, True)
print(pattern)
print(reverse_mapper(pattern))
text = io_library.reader(r'D:\Development\Encryption-Programs\Python\source\1.txt', 't')
freq = get_letter_frequency_order(text)
print(freq)
output = string_filler(text, pattern, freq)
word_freq = get_word_frequency_order(output, 'all')

print(output)
print(word_freq)
# target = fuck()
unordered_source = io_library.reader(r'dictionaries/english words unordered.json', 'j')
english_word_freq = io_library.reader(r'dictionaries/english words frequency.json', 'j')
print(type(english_word_freq))
print(english_word_freq)
print(1)
new_word_freq = []
new_eng_freq = []

for i in range(1, 4):
    eng_freq = english_word_freq[str(i + 1)]
    incorrect = []
    correct = []
    if len(word_freq[i]) != 0:
        for j in word_freq[i]:
            if j not in eng_freq:
                incorrect.append(j)
            else:
                correct.append(j)
    new_word_freq.append(tuple(incorrect))
    new_eng_freq.append(tuple(correct))

def freq_maper(string, incorrect, word_dict, pattern, reverse_pattern, index_dict):
    for i in incorrect:
        temp = list(i)
        for j in temp:
            if j[0] in word_dict:
                pass
            else:
                if j[0] == '_':
                    pass
                else:




print(new_word_freq)
print(new_eng_freq)
# ordered_source = io_library.reader(r'dictionaries/english words length ordered.json', 'j')

