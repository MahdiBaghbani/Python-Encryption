
from lib import io_library
from lib.FrequencyAnalyzer import alphabetical_sort

two = io_library.reader(r"dictionaries/english_two.json", 'j')
three = io_library.reader(r"dictionaries/english_three.json", 'j')
four = io_library.reader(r"dictionaries/english_four.json", 'j')
alpha = alphabetical_sort(two)
alpha = alphabetical_sort(two, True, alpha)
alpha = alphabetical_sort(three, dictionary=alpha)
alpha = alphabetical_sort(three, True, alpha)
alpha = alphabetical_sort(four, dictionary=alpha)
alpha = alphabetical_sort(four, True, alpha)
# for i in alpha:
#     q = dict()
#     q[2] = []
#     q[3] = []
#     q[4] = []
#     for j in alpha[i]:
#         q[len(j)].append(j)
#     alpha[i] = q
#
#
# print(alpha)
io_library.writer(r"dictionaries/english_words_unordered.json", alpha, 'j')

