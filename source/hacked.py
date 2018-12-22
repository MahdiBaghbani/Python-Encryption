from lib import FrequencyAnalyzer
from lib import io_library
from lib.Characters import LETTERS, ETAOIN_ALL, ETAOIN

a = {'A': set(), 'B': set(), 'C': set(), 'D': {'D'}, 'E': {'L'}, 'F': {'N'}, 'G': {'H'}, 'H': set(), 'I': set(),
     'J': {'O'}, 'K': set(), 'L': set(), 'M': {'T'}, 'N': {'Q'}, 'O': {'B'}, 'P': set(), 'Q': {'Q'}, 'R': {'Q'},
     'S': set(), 'T': set(), 'U': {'X'}, 'V': set(), 'W': {'G'}, 'X': {'Q'}, 'Y': {'E'}, 'Z': {'Z'}, 'a': {'Q'},
     'b': {'Q'}, 'c': set(), 'd': set(), 'e': {'H'}, 'f': {'Q'}, 'g': set(), 'h': {'M'}, 'i': {'B'}, 'j': {'U'},
     'k': set(), 'l': {'Q'}, 'm': set(), 'n': {'Z'}, 'o': {'W'}, 'p': set(), 'q': {'K'}, 'r': {'E'}, 's': set(),
     't': {'F'}, 'u': set(), 'v': set(), 'w': set(), 'x': set(), 'y': {'P'}, 'z': {'I'}, '!': set(), '"': set(),
     '#': {'S'}, '$': {'Q'}, '%': {'D'}, '&': {'A'}, "'": {'B'}, '(': {'W'}, ')': {'C'}, '*': {'W'}, '+': set(),
     ',': set(), '-': {'R'}, '.': {'E'}, '/': {'V'}, '0': set(), '1': {'J'}, '2': set(), '3': {'Q'}, '4': {'K'},
     '5': set(), '6': {'C'}, '7': set(), '8': {'A'}, '9': set(), ':': {'Y'}, ';': {'Y'}, '<': set(), '=': {'K'},
     '>': {'Q'}, '?': {'Q'}, '@': set(), '[': set(), '\\': set(), ']': {'Q'}, '^': {'Z'}, '_': {'W'}, '{': set(),
     '|': {'Q'}, '}': set(), '~': set(), ' ': set()}

index = {'A': list(), 'B': list(), 'C': list(), 'D': list(), 'E': list(), 'F': list(), 'G': list(), 'H': list(),
         'I': list(),
         'J': list(), 'K': list(), 'L': list(), 'M': list(), 'N': list(), 'O': list(), 'P': list(), 'Q': list(),
         'R': list(),
         'S': list(), 'T': list(), 'U': list(), 'V': list(), 'W': list(), 'X': list(), 'Y': list(), 'Z': list(),
         'a': list(),
         'b': list(), 'c': list(), 'd': list(), 'e': list(), 'f': list(), 'g': list(), 'h': list(), 'i': list(),
         'j': list(),
         'k': list(), 'l': list(), 'm': list(), 'n': list(), 'o': list(), 'p': list(), 'q': list(), 'r': list(),
         's': list(),
         't': list(), 'u': list(), 'v': list(), 'w': list(), 'x': list(), 'y': list(), 'z': list(), '!': list(),
         '"': list(),
         '#': list(), '$': list(), '%': list(), '&': list(), '\'': list(), '(': list(), ')': list(), '*': list(),
         '+': list(),
         ',': list(), '-': list(), '.': list(), '/': list(), '0': list(), '1': list(), '2': list(), '3': list(),
         '4': list(),
         '5': list(), '6': list(), '7': list(), '8': list(), '9': list(), ':': list(), ';': list(), '<': list(),
         '=': list(),
         '>': list(), '?': list(), '@': list(), '[': list(), '\\': list(), ']': list(), '^': list(), '_': list(),
         '{': list(),
         '|': list(), '}': list(), '~': list(), ' ': list()}

rep = {'A': list(), 'B': list(), 'C': list(), 'D': list(), 'E': list(), 'F': list(), 'G': list(), 'H': list(),
       'I': list(),
       'J': list(), 'K': list(), 'L': list(), 'M': list(), 'N': list(), 'O': list(), 'P': list(), 'Q': list(),
       'R': list(),
       'S': list(), 'T': list(), 'U': list(), 'V': list(), 'W': list(), 'X': list(), 'Y': list(), 'Z': list(),
       'a': list(),
       'b': list(), 'c': list(), 'd': list(), 'e': list(), 'f': list(), 'g': list(), 'h': list(), 'i': list(),
       'j': list(),
       'k': list(), 'l': list(), 'm': list(), 'n': list(), 'o': list(), 'p': list(), 'q': list(), 'r': list(),
       's': list(),
       't': list(), 'u': list(), 'v': list(), 'w': list(), 'x': list(), 'y': list(), 'z': list(), '!': list(),
       '"': list(),
       '#': list(), '$': list(), '%': list(), '&': list(), '\'': list(), '(': list(), ')': list(), '*': list(),
       '+': list(),
       ',': list(), '-': list(), '.': list(), '/': list(), '0': list(), '1': list(), '2': list(), '3': list(),
       '4': list(),
       '5': list(), '6': list(), '7': list(), '8': list(), '9': list(), ':': list(), ';': list(), '<': list(),
       '=': list(),
       '>': list(), '?': list(), '@': list(), '[': list(), '\\': list(), ']': list(), '^': list(), '_': list(),
       '{': list(),
       '|': list(), '}': list(), '~': list(), ' ': list()}


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


txt = io_library.reader('cipher/1.txt', 't', )
# txt = txt.replace('5', ' ')
f = FrequencyAnalyzer.get_letter_frequency_order(txt)
print(f)
out = ['_'] * len(txt)
for letter in LETTERS:
    index[letter] = find(txt, letter)

for letter in LETTERS:
    if len(a[letter]) == 1:
        rep[next(iter(a[letter]))].append(letter)

print(ETAOIN[1:7])
order = ETAOIN[1:7]
cip = f[1:9]
print(cip)
for i in order:
    c = []
    for t in rep[i]:
        if t in cip:
            c.append(t)
    rep[i] = c

for i in order:
    if len(rep[i]) == 1:
        k = list(cip)
        k.remove(rep[i][0])
        cip = ''.join(k)
print(cip)

for i in order:
    gg = cip[0]
    print(i)
    print(len(rep[i]))
    if len(rep[i]) == 0:
        print(rep[i])
        rep[i].append(gg)
        print(rep[i])
        print(rep)
    for letter in LETTERS:
        if len(rep[letter]) >= 1 and letter not in order:
            for y in rep[letter]:
                if y == gg:
                    rep[letter].remove(y)
print(rep)
print(cip)
for letter in LETTERS:
    if len(rep[letter]) == 1:
        for i in index[rep[letter][0]]:
            out[i] = letter
    elif len(rep[letter]) > 1:
        o = list()
        for i in rep[letter]:
            o.append(ETAOIN_ALL.index(i))
        s = min(o)
        for i in index[ETAOIN_ALL[s]]:
            out[i] = letter

for i in index[' ']:
    if out[i] == '_':
        out[i] = ' '

print(rep)

"""for letter in LETTERS:
    if len(a[letter]) == 1:
        s = next(iter(a[letter]))
        txt = txt.replace(letter, s)"""
o = ''.join(out)
io_library.writer('txt2.txt', o, 't')
