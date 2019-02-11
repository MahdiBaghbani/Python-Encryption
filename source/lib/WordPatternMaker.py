from lib import io_library


def make_word_pattern(dictionary_path: str, output_path: str, title: bool = True):
    all_patterns = dict()
    word_list = io_library.reader(dictionary_path, 'j')
    make_pattern_dictionary(word_list, all_patterns, title)

    # dump pattern dictionary into a json file
    io_library.writer(output_path, all_patterns, 'j')


def make_pattern_dictionary(word_list: list, pattern_dict: dict, title: bool):
    """ Function to make a dictionary mapping patterns to words"""

    complete_list = list()

    for word in word_list:
        complete_list.append(word.upper())
        if title and len(word) != 1:
            complete_list.append(word.title())

    for word in complete_list:
        pattern = get_word_pattern(word)
        if pattern not in pattern_dict:
            pattern_dict[pattern] = [word]
        else:
            pattern_dict[pattern].append(word)


def get_word_pattern(word: str) -> str:
    """ Function to generate a word pattern"""

    next_num = 0
    letter_nums = dict()
    word_pattern = list()

    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])

    return '.'.join(word_pattern)
