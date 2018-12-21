from collections import defaultdict

from lib import WordPatternMaker
from lib.Characters import LETTERS


def frequency_aided_mapper(pattern: dict, word_frequency: str, complex_frequency: tuple):
    pass


def pattern_mapper(string: str, pattern_dictionary: dict) -> dict:
    """ Function to produce letter mapping for an string"""
    intersected_map = blank_mapper_dict()
    word_list = string.split()
    for word in word_list:
        new_map = blank_mapper_dict()
        word_pattern = WordPatternMaker.get_word_pattern(word)
        if word_pattern not in pattern_dictionary:
            continue
        for candidate in pattern_dictionary[word_pattern]:
            # adds word mapping of each candidate word to new_map dictionary
            add_letters_to_mapping(new_map, word, candidate)

        intersected_map = intersect_mappings(intersected_map, new_map)

    return remove_solved_letters_from_mapping(intersected_map)


def blank_mapper_dict() -> dict:
    """ Function that returns a dictionary containing
        all letters as keys and blank set as value"""

    dictionary = defaultdict(set)
    # populate dictionary
    for letter in LETTERS:
        dictionary[letter]
    return dictionary


def add_letters_to_mapping(letter_mapping: dict, string: str, candidate: list):  # -> dict:
    """ Function to create map between a string and its candidate"""
    for i in range(len(string)):
        letter_mapping[string[i]].add(candidate[i].upper())


def intersect_mappings(map_a: dict, map_b: dict) -> dict:
    """ Function to calculate intersected mappings out of 2 maps"""
    # new mapper dictionary
    intersected_mapping = blank_mapper_dict()

    for letter in LETTERS:
        # if map_a[letter] is empty, copy map_b[letter] into intersected mapping
        if not map_a[letter]:
            intersected_mapping[letter] = set_copy(map_b[letter])
        # if map_b[letter] is empty, copy map_a[letter] into intersected mapping
        # if both map_a and map_b are empty then the intersected mapping will be empty
        elif not map_b[letter]:
            intersected_mapping[letter] = set_copy(map_a[letter])
        # if map_a and map_b both has values, then only copy the values that two maps
        # have in common in "both" maps into intersected mapper
        else:
            for mapped_letter in map_a[letter]:
                if mapped_letter in map_b[letter]:
                    intersected_mapping[letter].add(mapped_letter)

    return intersected_mapping


def remove_solved_letters_from_mapping(letter_mapping: dict) -> dict:
    """
    Letters in the mapping that map to only one letter are
    "solved" and can be removed from the other letters.
    For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    maps to ['N'], then we know that 'B' must map to 'N', source we can
    remove 'N' from the list of what 'A' could map to. So 'A' then maps
    to ['M']. Note that now that 'A' maps to only one letter, we can
    remove 'M' from the list of potential letters for every other
    key. (This is why there is a loop that keeps reducing the map.)
    """
    # loop
    loop = True
    while loop:
        # first assume that we will not loop again
        loop = False
        # solvedLetters will be a list of letters that have one
        # and only one possible mapping in letter_mapping
        solved_letters = list()
        # loop through letters and find solved ones
        for letter in LETTERS:
            if len(letter_mapping[letter]) == 1:
                # append letter to solved letters
                solved_letters.append(next(iter(letter_mapping[letter])))
        # loop through letters and remove solved ones from mapping
        for letter in LETTERS:
            for solved in solved_letters:
                if len(letter_mapping[letter]) != 1 and solved in letter_mapping[letter]:
                    letter_mapping[letter].remove(solved)

                    # A new letter is now solved, source loop again.
                    if len(letter_mapping[letter]) == 1:
                        loop = True

    return letter_mapping


def set_copy(input_set: set) -> set:
    """ Function to deep copy a set object """
    return {i for i in input_set}
