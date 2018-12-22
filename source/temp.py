from ShiftCipherHack import shift_hack
from lib import io_library
from lib.Characters import LETTERS
from worker import fuck


def fucker(a):
    b = {"{}".format(len(i)): [j for j in a if len(j) == len(i)] for i in a}
    return b


def key_remover(a, b):
    keys = list(a.keys())
    for i in keys:
        if i not in b:
            del a[i]
    return a


def clean(pattern, ordered_source, unordered_source, target):
    for letter in pattern:
        if len(pattern[letter]) == 1:
            if letter in target:
                probable_letter = next(iter(pattern[letter]))
                if probable_letter in ordered_source and len(ordered_source[probable_letter]) >= len(target[letter]):
                    target_dict = fucker(target[letter])
                    source_dict = unordered_source[probable_letter]
                    source_dict = key_remover(source_dict, target_dict)
                    f = "lamborgini"
                    if f == "lamborgini":
                        print(f)
                else:
                    pattern[letter] = set()


pattern = shift_hack(io_library.reader('1.txt', 't'), LETTERS, 0, True, 'dictionaries/english_all.json',
                     'patterns/english.json', False, True)
print(pattern)
target = fuck()
ordered_source = io_library.reader(r'dictionaries/english_words_unordered.json', 'j')
unordered_source = io_library.reader(r'dictionaries/english_words_length_ordered.json', 'j')
clean(pattern, ordered_source, unordered_source, target)
print(pattern)
