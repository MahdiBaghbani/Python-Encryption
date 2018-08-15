import pprint

import io_library


def main():
   make_word_pattern()


def get_word_pattern(word):
    next_num = 0
    letter_nums = dict()
    word_pattern = list()

    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_pattern.append(letter_nums[letter])

    return '.'.join(word_pattern)


def make_pattern_dictionary(word_list: str, pattern_dict: dict, title: bool):
    for word in word_list:
        if title:
            word = word.title()
        else:
            word = word.upper()
        pattern = get_word_pattern(word)
        if pattern not in pattern_dict:
            pattern_dict[pattern] = [word]
        else:
            pattern_dict[pattern].append(word)


def make_word_pattern():
    all_patterns = dict()
    word_list = io_library.reader('dictionary_en.txt', 't').split('\n')
    make_pattern_dictionary(word_list, all_patterns, False)
    make_pattern_dictionary(word_list, all_patterns, True)

    fo = open('wordPatternsTitle.py', 'w')
    fo.write('allPatterns = ')
    fo.write(pprint.pformat(all_patterns))
    fo.close()


if __name__ == '__main__':
    main()
