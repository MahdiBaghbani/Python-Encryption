from collections import defaultdict

from lib import TrueTextDetector
from lib import WordPatternMaker
from lib.Characters import NEW_LINE, ETAOIN


def pattern_mapper(string: str, pattern_dictionary: dict, space_letter: str, letter_sequence: str) -> dict:
    """
    Function to produce letter mapping for an string

    :param string: text to be mapped to letters from pattern dictionary
    :param pattern_dictionary: a dictionary of WORD PATTERNS
    :param space_letter: this identifies space letter in text, so we can use
     .split function to get a list words out of raw text
    :param letter_sequence: a string containing all letters used in the string
    :return mapping dictionary
    """

    # check inputs
    if not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")
    if not type(pattern_dictionary) == dict:
        raise TypeError("Argument 'pattern_dictionary' of this function must be of type dictionary.\n")

    # initialize the a blank intersected map
    intersected_map = blank_mapper_dict()
    # split string text into words
    word_list = string.split(space_letter)
    # find mapping for each word in the string text
    for word in word_list:
        new_map = blank_mapper_dict()
        word_pattern = WordPatternMaker.get_word_pattern(word)
        if word_pattern not in pattern_dictionary:
            continue
        for candidate in pattern_dictionary[word_pattern]:
            # adds word mapping of each candidate word to new_map dictionary
            add_letters_to_mapping(new_map, word, candidate)
        # intersect new map with previous intersected map
        intersected_map = intersect_mappings(intersected_map, new_map, letter_sequence)
    # add space letter to the pattern map
    intersected_map[space_letter].add(' ')

    # return solved mapping dictionary
    return dict(remove_solved_letters_from_mapping(intersected_map, letter_sequence))


def blank_mapper_dict() -> defaultdict:
    """
    Function that returns a default dictionary with values of type set
    """

    return defaultdict(set)


def add_letters_to_mapping(letter_map: defaultdict, string: str, candidate: str):
    """
    Function to create map between a string and its candidate
    :param letter_map: mapping to be completed
    :param string: word
    :param candidate: candidate word for the word
    """

    # check inputs
    if not (type(string) == str and type(candidate) == str):
        raise TypeError("Arguments 'string' and 'candidate' of this function must be of type string.\n")
    if not type(letter_map) == defaultdict:
        raise TypeError("Argument 'letter_map' of this function must be of type default dictionary.\n")

    # add each letter of candidate to corresponding word letter map
    for i in range(len(string)):
        letter_map[string[i]].add(candidate[i].upper())


def intersect_mappings(letter_map_a: defaultdict, letter_map_b: defaultdict, letter_sequence: str) -> defaultdict:
    """
    Function to calculate intersected mappings out of 2 maps

    :param letter_map_a: first map
    :param letter_map_b: second map
    :param letter_sequence: a string containing all letters used in the string
    :return: intersected map from first and second map

    """

    # check inputs
    if not (type(letter_map_a) == defaultdict and type(letter_map_b) == defaultdict):
        raise TypeError("Arguments of this function must be of type default dictionary.\n")

    # new mapper dictionary
    intersected_mapping = blank_mapper_dict()

    for letter in letter_sequence:
        # if letter_map_a[letter] is empty, copy letter_map_b[letter] into intersected mapping
        if not letter_map_a[letter]:
            intersected_mapping[letter] = shallow_set_copy(letter_map_b[letter])
        # if letter_map_b[letter] is empty, copy letter_map_a[letter] into intersected mapping
        # if both letter_map_a and letter_map_b are empty then the intersected mapping will be empty
        elif not letter_map_b[letter]:
            intersected_mapping[letter] = shallow_set_copy(letter_map_a[letter])
        # if letter_map_a and letter_map_b both has values, then only copy the values that two maps
        # have in common in "both" maps into intersected mapper
        else:
            for mapped_letter in letter_map_a[letter]:
                if mapped_letter in letter_map_b[letter]:
                    intersected_mapping[letter].add(mapped_letter)

    return intersected_mapping


def remove_solved_letters_from_mapping(letter_map: defaultdict, letter_sequence: str) -> defaultdict:
    """
    Letters in the mapping that map to only one letter are
    "solved" and can be removed from the other letters.
    For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    maps to ['N'], then we know that 'B' must map to 'N', source we can
    remove 'N' from the list of what 'A' could map to. So 'A' then maps
    to ['M']. Note that now that 'A' maps to only one letter, we can
    remove 'M' from the list of potential letters for every other
    key. (This is why there is a loop that keeps reducing the map.)

    :param letter_map: the dictionary containing mapping between letters
    :param letter_sequence: a string containing all letters used in the string
    :return cleared mapping
    """

    # check inputs
    if not type(letter_map) == defaultdict:
        raise TypeError("Argument of this function must be of type default dictionary.\n")

    # loop
    loop = True
    while loop:
        # first assume that we will not loop again
        loop = False
        # solvedLetters will be a list of letters that have one
        # and only one possible mapping in letter_map
        solved_letters = list()
        # loop through letters and letter_index_finder solved ones
        for letter in letter_sequence:
            if len(letter_map[letter]) == 1:
                # append letter to solved letters
                solved_letters.append(next(iter(letter_map[letter])))
        # loop through letters and remove solved ones from mapping
        for letter in letter_sequence:
            for solved in solved_letters:
                if len(letter_map[letter]) != 1 and solved in letter_map[letter]:
                    letter_map[letter].remove(solved)

                    # A new letter is now solved, source loop again.
                    if len(letter_map[letter]) == 1:
                        loop = True

    return letter_map


def repair_mapping(letter_map: dict, aid_map: dict, letter_sequence: str) -> dict:
    """
    Function to repair an existing mapping with ais dictionary

    :param letter_map: original mapping
    :param aid_map: aid mapping that will be used to repair the original mapping
    :param letter_sequence: the letters that has been used in the string which original mapping derived
    :return: repaired apping
    """

    # create a new default dictionary
    repaired_dict = blank_mapper_dict()

    # replace values of aid map into the original dictionary
    for key in aid_map:
        letter_map[key] = aid_map[key]

    # convert original dictionary into default dictionary
    for key in letter_map:
        repaired_dict[key] = letter_map[key]

    # remove solved letters if possible and return a repaired dictionary
    return dict(remove_solved_letters_from_mapping(repaired_dict, letter_sequence))


def index_mapper(string: str, mode: str, letter_sequence: str, word=None):
    """
     Function to create a dictionary that maps every letter
     to a list of indexes of its occurrence in a given string
     or return a list of indexes of first letter occurrences of a given word

     :param string: string source
     :param mode: 'letter' or 'word'
     :param letter_sequence: a string containing all letters used in the string
     :param word: the target word for finding indexes
     :return: dictionary when mode = 'letter' and list when mode = 'word'

     """

    # check inputs
    if not (type(string) == str and type(mode) == str):
        raise TypeError("Arguments of this function must be of type string.\n")

    # map letters
    if mode == "letter":
        # adding new line character '\n' to letter_sequence
        letters = letter_sequence + NEW_LINE
        # a default dictionary containing the list as key
        index = defaultdict(list)
        for letter in letters:
            index[letter] = letter_index_finder(string, letter)
        # return normal dictionary instead of default dict
        return dict(index)
    # map words
    elif mode == "word" and word:
        # check input
        if not type(word) == str:
            raise TypeError("word argument must be of type string.\n")
        # a default dictionary containing the list as key
        all_indexes = defaultdict(list)
        # find indexes of letters in the word
        for letter in word:
            all_indexes[letter] = letter_index_finder(string, letter)
        # result is indexes of first letter of word in string
        index = all_indexes[word[0]]
        # list of indexes that must be omitted from above list
        #  because they are first letter of given word
        #  but the word didn't come after them
        remove_list = list()
        word_length = len(word)
        # loop for finding incorrect indexes
        # imagine word "Capital", for each occurrence index of "C" for example "i",
        # there must be and occurrence of index "p" which is "i + 2" and
        # occurrences of indexes "a" which must be "i + 1" and "i + 5", this must be true for all letters in word
        # if one index is mismatched then the index "i" of word "C", can't be start of word "Capital"
        # and therefore must be removed
        for i in index:
            for j in range(1, word_length):
                if i + j not in all_indexes[word[j]]:
                    remove_list.append(i)
        # remove wrong indexes
        for i in remove_list:
            index.remove(i)
        # return list of correct indexes
        return index
    # raise error
    else:
        raise AttributeError("Function mode is wrong. it must be either 'letter' or 'word'.\n")


def letter_index_finder(string: str, character: str) -> list:
    """
    Function to return index of every occurrence of a given character in a string

    :param string: input string
    :param character: character
    :return: list containing index
    """

    # check inputs
    if not (type(string) == str and type(character) == str):
        raise TypeError("Arguments of this function must be of type string.\n")
    # return index list
    return [i for i, ltr in enumerate(string) if ltr == character]


def get_word_from_index(string: str, index: int) -> str:
    """
    This function takes a string and an index, then will return
    a word in the string that has a letter corresponding to that index
    for example string 'Lulu is a cute girl" and index "5", the fifth element
     in string is "i" this function will return the word containing "i" which is "is"

    :param string: input string
    :param index: an index of a letter of a word in the input string
    :return: return a string containing required word
    """

    # check inputs
    if not (type(string) == str and type(index) == int):
        raise TypeError("Arguments of this function have wrong type.\n")
    # list indexes of all spaces in the string
    space_index = letter_index_finder(string, ' ')
    # if the given index is not in space_index then it's not a space and is a letter
    if index not in space_index:
        # find right and left spaces of given index
        right_space_indexes = [i for i in space_index if i > index]
        left_space_indexes = [i for i in space_index if i < index]

        # if right spaces exist then find the nearest right space
        if right_space_indexes:
            right_space = min(right_space_indexes)
        # if left spaces exist then find the nearest left space
        if left_space_indexes:
            left_space = max(left_space_indexes)

        # right and left spaces exist so the word in between them
        if right_space_indexes and left_space_indexes:
            return string[left_space + 1:right_space]
        # left space doesn't exist so the word is in the beginning of the string
        elif right_space_indexes:
            return string[0:right_space]
        # right space doesn't exist so the word is at the end of string
        elif left_space_indexes:
            return string[left_space + 1:-1]
    # index is on the space_index so the required word is a space
    return string[index]


def string_filler(letter_map: dict, letter_index_map: dict, string_length: int = None, string: str = None) -> list:
    """
    This function will create a string and fill it with letters on a letter map
    based on their indexes in the letter index map, it can also
    refill an existing string with same requirements, but the
    letter index map must be compatible [do not cause IndexError in process]

    :param letter_map: mapping of letters
    :param letter_index_map: indexes of each letter in letter map
    :param string_length: length of output string
    :param string: existing string to be refilled
    :return: a list containing filled letters
    """

    # check inputs
    if not (type(letter_map) == dict and type(letter_index_map) == dict):
        raise TypeError("Arguments 'letter_map' and 'letter_index_map' of this function must be of type dictionary.\n")
    if string_length and not type(string_length) == int:
        raise TypeError("Argument 'string_length' of this function must be of type integer.\n")
    if string and not type(string) == str:
        raise TypeError("Argument 'string' of this function must be of type string.\n")

    # determine to use an existing string or create new string
    if string:
        # convert string into list of letters
        output_string = list(string)
    else:
        # create a blank text with length equal to cipher-text
        output_string = ['_'] * string_length

    # loop to reconstruct plain-txt from solved cipher-letters
    for letter in letter_map:
        # if the cipher-letter "letter" is solved, it's corresponding set must be of size 1
        if len(letter_map[letter]) == 1:
            # extract plain-letter from set inside dictionary
            plain_letter = next(iter(letter_map[letter]))
            # use indexes of cipher-letter "letter" in cipher-text to place plain-letter in correct position
            for i in letter_index_map[letter]:
                # it is possible to catch IndexError for un-compatible letter_index_map and string
                try:
                    output_string[i] = plain_letter
                except IndexError:
                    raise IndexError("'letter_index_map' argument isn't compatible with 'string' argument!\n")
    # return filled string
    return output_string


def test_high_frequency(string: str, output_string: str, pattern: dict, letter_index_map: dict, letter_sequence: str,
                        frequent_words: dict, words: set) -> dict:
    """
    This function tests the decrypted text based on high-frequency cipher-letters
    to see if they are correctly decrypted into plain-letters, and if finds wrong ones,
    will try to decrypt them to correct plain-letters if possible

    :param string: cipher-text [spaces must have been decrypted and replaced]
    :param output_string: plain-text that is to be examined
    :param pattern: pattern map for decryption
    :param letter_index_map: letter indexes of cipher-letters
    :param letter_sequence: first 6 most frequent cipher-letters [excluding space]
    :param frequent_words: a dictionary of most frequent english words with keys of letters
    example {E: [THE, WE], W: [WE]}
    :param words: a set of english words
    :return: a dictionary that maps a cipher-letter to a plain-letter
    """

    # check inputs
    if not (type(string) == str and type(output_string) == str and type(letter_sequence) == str):
        raise TypeError("Arguments 'string' and 'output_string' and 'letter_sequence' "
                        "of this function must be of type string.\n")
    if not (type(pattern) == dict and type(letter_index_map) == dict and type(frequent_words) == dict):
        raise TypeError("Arguments 'pattern' and 'letter_index_map' and 'frequent_words' "
                        "of this function must be of type dictionary.\n")
    if not type(words) == set:
        raise TypeError("Argument 'words' of this function must be of type set.\n")

    # TODO ETAOIN must be replaced by an argument variable, [to support other languages as well]
    # list most frequent English characters
    candidates = list(ETAOIN[1:7])
    # get high frequency letters
    high_frequency = letter_sequence[1:7]
    # initializing dictionaries
    repaired = defaultdict(set)
    test_dictionary = defaultdict(list)

    # TODO document this part, [HELL NO! I can explain it to anyone with voice but I just don't want to write it]
    for letter in high_frequency:
        test_word_list = list()
        for index in letter_index_map[letter]:
            test_word_list.append([
                index_mapper(get_word_from_index(string, index), 'letter', letter_sequence),
                get_word_from_index(output_string, index)
            ])
        if not TrueTextDetector.is_true_text(' '.join([test_case[1] for test_case in test_word_list]), words):
            test_dictionary[letter] = [
                test_case for test_case in test_word_list
                if len(test_case[1]) == 2 or len(test_case[1]) == 3 or len(test_case[1]) == 4
            ]
        else:
            try:
                candidates.remove(next(iter(pattern[letter])))
            except ValueError:
                pass

    for letter in test_dictionary:
        for candidate in candidates:
            candidate_word_set = set()
            candidate_case_list = test_dictionary[letter]
            for case in candidate_case_list:
                letter_list = list(case[1])
                for index in case[0][letter]:
                    letter_list[index] = candidate
                candidate_word_set.add(''.join(letter_list))

            # test if match with correct English
            counter = 0
            for word in candidate_word_set:
                if word in frequent_words[candidate]:
                    counter += 1
            # if more than 50% was correct, assign the candidate to cipher letter
            #  and remove candidate from future loop
            # TODO replace the hard coded 0.5 value with a variable
            if len(candidate_word_set) != 0 and counter / len(candidate_word_set) > 0.5:
                repaired[letter].add(candidate)
                candidates.remove(candidate)
                break
    # return repaired cipher-letter to plain-letter dictionary
    return dict(repaired)


def shallow_set_copy(input_set: set) -> set:
    """
    Function to shallow copy a set object

    :param input_set: the set to be copied
    :return a new set exactly like the original set
    """

    # check inputs
    if not type(input_set) == set:
        raise TypeError("Argument of this function must be of type set.\n")

    return {i for i in input_set}
