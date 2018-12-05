dictionary = dict()
source = dict()
target = dict()
for letter in dictionary:
    if len(dictionary[letter]) == 1:
        if letter in target:
            probable_letter = next(iter(dictionary[letter]))
            if probable_letter in source:
                pass
            else:
                dictionary[letter] = set()




