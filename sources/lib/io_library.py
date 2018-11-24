import os.path as opath
import pickle
from itertools import islice


def check_path(path: str):
    if not opath.isfile(path):
        raise FileNotFoundError


def reader(path: str, mode: str, max_lines: int = 0, encoding: str = 'utf-8'):
    """ Wrapper for various methods to read data from a file

    :param path: path to the file
    :param mode: 't' for text file, 'b' for binary and 'p' for pickle
    :param max_lines: max lines to be read from a file
    :param encoding: text encodings for decode
    :return: read content
    """

    def text_reader(p: str, l: int, e: str) -> str:
        """ Reads in all of a textual file """
        with open(p, 'r', encoding=e) as read:
            if l:
                data = list(islice(read, l))
                data = ''.join(data)
            else:
                data = read.read()
        return data

    def binary_reader(p: str):
        """ Reads in all of a file in binaries """

        with open(p, 'rb') as read:
            data = read.read()
        return data

    def pickle_reader(p: str):
        with open(p, 'rb') as read:
            data = pickle.loads(read.read())
        return data

    check_path(path)

    if mode is 't':
        return text_reader(path, max_lines, encoding)
    elif mode is 'b':
        return binary_reader(path)
    elif mode is 'p':
        return pickle_reader(path)


def writer(path: str, data, mode: str, encoding: str = 'utf-8'):
    """ Wrapper for various methods to write data to a file
    :param path: path to the file
    :param data: data to be writen in file
    :param mode: 't' for text file, 'b' for binary and 'p' for pickle
    :param encoding: text encodings for decode
    """

    def text_writer(p: str, d, e: str):
        """ Writes out text to a file """

        with open(p, 'w+', encoding=e) as write:
            write.write(d)

    def binary_writer(p, d):
        """ Writes out binaries to a file """

        with open(p, 'wb') as write:
            write.write(d)

    def pickle_writer(p, d):
        """ Writes out a data serialized content in a file """

        with open(p, 'wb+') as write:
            pickle.dump(d, write, pickle.HIGHEST_PROTOCOL)

    if mode is 't':
        text_writer(path, data, encoding)
    elif mode is 'b':
        binary_writer(path, data)
    elif mode is 'p':
        pickle_writer(path, data)
