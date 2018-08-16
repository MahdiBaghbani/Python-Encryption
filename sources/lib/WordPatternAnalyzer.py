import copy
from lib.Characters import LETTERS
from lib import MakeWordPattern
from lib import wordPatterns


def main():
    pass


def get_blank_cipherletter_mapping() -> dict:
    return {'A': set(), 'B': set(), 'C': set(), 'D': set(), 'E': set(), 'F': set(), 'G': set(), 'H': set(), 'I': set(),
            'J': set(), 'K': set(), 'L': set(), 'M': set(), 'N': set(), 'O': set(), 'P': set(), 'Q': set(), 'R': set(),
            'S': set(), 'T': set(), 'U': set(), 'V': set(), 'W': set(), 'X': set(), 'Y': set(), 'Z': set(), 'a': set(),
            'b': set(), 'c': set(), 'd': set(), 'e': set(), 'f': set(), 'g': set(), 'h': set(), 'i': set(), 'j': set(),
            'k': set(), 'l': set(), 'm': set(), 'n': set(), 'o': set(), 'p': set(), 'q': set(), 'r': set(), 's': set(),
            't': set(), 'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': set(), 'z': set(), '!': set(), '"': set(),
            '#': set(), '$': set(), '%': set(), '&': set(), '\'': set(), '(': set(), ')': set(), '*': set(), '+': set(),
            ',': set(), '-': set(), '.': set(), '/': set(), '0': set(), '1': set(), '2': set(), '3': set(), '4': set(),
            '5': set(), '6': set(), '7': set(), '8': set(), '9': set(), ':': set(), ';': set(), '<': set(), '=': set(),
            '>': set(), '?': set(), '@': set(), '[': set(), '\\': set(), ']': set(), '^': set(), '_': set(), '{': set(),
            '|': set(), '}': set(), '~': set(), ' ': set()}


def add_letters_to_mapping(letter_mapping: dict, cipher_word: str, candidate: list):
    letter_mapping = copy.deepcopy(letter_mapping)
    for i in range(len(cipher_word)):
        letter_mapping[cipher_word[i]].add(candidate[i].upper())

    return letter_mapping


def intersect_mappings(map_a: dict, map_b: dict) -> dict:
    intersected_mapping = get_blank_cipherletter_mapping()
    for letter in LETTERS:
        if not map_a[letter]:
            intersected_mapping[letter] = copy.deepcopy(map_b[letter])
        elif not map_b[letter]:
            intersected_mapping[letter] = copy.deepcopy(map_a[letter])
        else:
            for mappedLetter in map_a[letter]:
                if mappedLetter in map_b[letter]:
                    intersected_mapping[letter].add(mappedLetter)

    return intersected_mapping


def remove_solved_letters_from_mapping(letter_mapping: dict):
    letter_mapping = copy.deepcopy(letter_mapping)
    loop_again = True
    while loop_again:
        loop_again = False
        solved_letters = list()
        for cipherletter in LETTERS:
            if len(letter_mapping[cipherletter]) == 1:
                solved_letters.append(next(iter(letter_mapping[cipherletter])))
        for cipherletter in LETTERS:
            for s in solved_letters:
                if len(letter_mapping[cipherletter]) != 1 and s in letter_mapping[cipherletter]:
                    letter_mapping[cipherletter].remove(s)
                    if len(letter_mapping[cipherletter]) == 1:
                        loop_again = True

    return letter_mapping


def hack_simple_sub(message):
    intersected_map = get_blank_cipherletter_mapping()
    cipher_word_list = message.split()
    for cipher_word in cipher_word_list:
        new_map = get_blank_cipherletter_mapping()
        word_pattern = MakeWordPattern.get_word_pattern(cipher_word)
        if word_pattern not in wordPatterns.allPatterns:
            continue
        for candidate in wordPatterns.allPatterns[word_pattern]:
            new_map = add_letters_to_mapping(new_map, cipher_word, candidate)

        intersected_map = intersect_mappings(intersected_map, new_map)

    return remove_solved_letters_from_mapping(intersected_map)


if __name__ == '__main__':
    main()
