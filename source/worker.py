from lib.FrequencyAnalyzer import get_letter_frequency_order, get_word_frequency_order, alphabetical_sort
from lib.io_library import reader, writer


def fuck():
    text = reader(r'D:\Development\Encryption-Programs\Python\source\1.txt', 't')
    freq = get_letter_frequency_order(text)
    text = text.replace(freq[0], ' ')
    word_tuple = get_word_frequency_order(text, 'all')

    dictionary = dict()
    for i in word_tuple:
        dictionary = alphabetical_sort(i, dictionary, both=True)

    return dictionary
    # print(dictionary)


def me():
    two = reader(r'dictionaries/english_two.json', 'j')
    three = reader(r'dictionaries/english_three.json', 'j')
    four = reader(r'dictionaries/english_four.json', 'j')
    allem = [two, three, four]
    dictionary = dict()
    for i in allem:
        dictionary = alphabetical_sort(i, dictionary, both=True)

    return dictionary

