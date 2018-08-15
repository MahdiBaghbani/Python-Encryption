from lib.Characters import LETTERS

ETAOIN_ALL = ' etaoinshrdlcumwfgypbvkjxqz,.TBHCM"1AG029I\'SLP4ENUW()-58ODFKZ6;RYVJXQ!#$%&*+/37:<=>?@[\]^_{|}~'
ETAOIN = ' ETAOINSHRDLCUMWFGYPBVKJXQZ'

englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I':
    6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C':
                         2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P':
                         1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z':
                         0.07}


def get_letter_count(message):
    letter_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
                    'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                    'Y': 0, 'Z': 0, 'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0,
                    'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0,
                    'w': 0, 'x': 0, 'y': 0, 'z': 0, '!': 0, '"': 0, '#': 0, '$': 0, '%': 0, '&': 0, '\'': 0, '(': 0,
                    ')': 0, '*': 0, '+': 0, ',': 0, '-': 0, '.': 0, '/': 0, '0': 0, '1': 0, '2': 0, '3': 0, '4': 0,
                    '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, ':': 0, ';': 0, '<': 0, '=': 0, '>': 0, '?': 0, '@': 0,
                    '[': 0, '\\': 0, ']': 0, '^': 0, '_': 0, '{': 0, '|': 0, '}': 0, '~': 0, ' ': 0}
    for letter in message:
        if letter in LETTERS:
            letter_count[letter] += 1
    return letter_count


def get_frequency_order(message):
    letter_to_freq = get_letter_count(message)
    freq_to_letter = dict()
    for letter in LETTERS:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)
    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=ETAOIN_ALL.find, reverse=True)
        freq_to_letter[freq] = ''.join(freq_to_letter[freq])
    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=get_item_at_index_zero, reverse=True)
    freq_order = list()
    for freqPair in freq_pairs:
        freq_order.append(freqPair[1])
    return ''.join(freq_order)


def get_item_at_index_zero(x):
    return x[0]


def letter_mapper():
    pass


def english_freq_match_score(message):
    freq_order = get_frequency_order(message)
    freq_order = freq_order.upper()
    match_score = 0
    for commonLetter in ETAOIN[:7]:
        if commonLetter in freq_order[:7]:
            match_score += 1
    for uncommonLetter in ETAOIN[-7:]:
        if uncommonLetter in freq_order[-73: -67]:
            match_score += 1

    return match_score
