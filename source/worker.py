from lib import io_library
from lib.FrequencyAnalyzer import get_letter_frequency_order, get_word_frequency_order, alphabetical_sort
from lib.Characters import ETAOIN
from lib.WordPatternAnalyzer import pattern_mapper
#from ShiftCipherHack import analyze
from patterns.MakePattern import make_pattern
#string = io_library.reader(r"cipher/1.txt", 't')
#analyze(string)

# a = "Puppy"
# t = pattern_mapper(a)
# print(t)
# make_pattern('D:\Development\Encryption-Programs\Python\source\dictionaries\english_all.json',
#              'D:\Development\Encryption-Programs\Python\source\patterns\english.json')

# word_list = io_library.reader('D:\Development\Encryption-Programs\Python\source\dictionaries\english_all.txt',
#                               't').split('\n')
# r = []
# for i in word_list:
#     r.append(i.upper())
# io_library.writer('D:\Development\Encryption-Programs\Python\source\dictionaries\english_all.json', r, 'j')

string = io_library.reader(r"D:\Development\Encryption-Programs\Python\sources\texts\alan turing.txt", 't')
# print(string)
# freq = get_letter_frequency_order(string)
#
# print(freq)
# string = io_library.reader(r"cipher/alan turing.txt", 't')
# freq = get_letter_frequency_order(string)
#
# print(freq)
frequency = get_letter_frequency_order(string)
# replace the most frequent with ' ' [space], because in 99% of cases
# the most frequent character in a cipher_text in ' '
cipher_text = string.replace(frequency[0], ETAOIN[0])
wordfreq = get_word_frequency_order(cipher_text, 'all')
t = list(wordfreq[1])
t1 = alphabetical_sort(t)
t1 = alphabetical_sort(wordfreq[2], dictionary=t1)
t1 = alphabetical_sort(wordfreq[3], dictionary=t1)
t11 = alphabetical_sort(t, True)
#print(wordfreq)


string = io_library.reader(r"D:\Development\Encryption-Programs\Python\sources\cipher\1.txt", 't')
# print(string)
# freq = get_letter_frequency_order(string)
#
# print(freq)
# string = io_library.reader(r"cipher/alan turing.txt", 't')
# freq = get_letter_frequency_order(string)
#
# print(freq)
frequency = get_letter_frequency_order(string)

# replace the most frequent with ' ' [space], because in 99% of cases
# the most frequent character in a cipher_text in ' '
cipher_text = string.replace(frequency[0], ETAOIN[0])
wordfreq = get_word_frequency_order(cipher_text, 'all')
t = list(wordfreq[1])
t2 = alphabetical_sort(t)
t2 = alphabetical_sort(wordfreq[2], dictionary=t2)
t2 = alphabetical_sort(wordfreq[3], dictionary=t2)
t22 = alphabetical_sort(t, True)
#print(wordfreq)
#print(frequency)

alpha = io_library.reader(r"dictionaries/english_two.json", 'j')
alpha1 = alphabetical_sort(alpha)
alpha2 = alphabetical_sort(alpha, True)
#print(alpha1)
#print(alpha1.keys())
#print(alpha2)
#print(alpha2.keys())
#print()
print(t1)
print(t2)
print()
print(t11)
print(t22)