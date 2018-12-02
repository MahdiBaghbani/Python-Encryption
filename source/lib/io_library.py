import json
import pickle
import os.path as opath
from itertools import islice


def check_path(path: str):
    if not opath.isfile(path):
        raise FileNotFoundError


def reader(path: str, fmt: str, max_lines: int = 0, encoding: str = 'utf-8'):
    """ Wrapper for various methods to read data from a file

    :param path: path to the file
    :param fmt: 't' for text file, 'b' for binary,
                   'p' for pickle, 'j' for json
    :param max_lines: max lines to be read from a file
    :param encoding: text encodings for decode
    :return: read content
    """

    def text_reader(p: str, mxl: int, e: str) -> str:
        """ Reads in all of a textual file """
        with open(p, 'r', encoding=e) as file:
            if mxl:
                data = list(islice(file, mxl))
                data = ''.join(data)
            else:
                data = file.read()
        return data

    def binary_reader(p: str):
        """ Reads in all of a file in binaries """

        with open(p, 'rb') as file:
            data = file.read()
        return data

    def pickle_reader(p: str):
        """ Reads in a pickled file"""
        with open(p, 'rb') as file:
            data = pickle.loads(file.read())
        return data

    def json_reader(p: str):
        """ Reads in a json file"""
        with open(p, 'r') as file:
            data = json.load(file)
        return data

    check_path(path)

    if fmt is 't':
        return text_reader(path, max_lines, encoding)
    elif fmt is 'b':
        return binary_reader(path)
    elif fmt is 'p':
        return pickle_reader(path)
    elif fmt is 'j':
        return json_reader(path)
    else:
        raise ValueError("Format is not valid!\n")


def writer(path: str, data, fmt: str, encoding: str = 'utf-8'):
    """ Wrapper for various methods to write data to a file
    :param path: path to the file
    :param data: data to be writen in file
    :param fmt: 't' for text file, 'b' for binary,
                'p' for pickle, 'j' for json
    :param encoding: text encodings for decode
    """

    def text_writer(p: str, d, e: str):
        """ Writes out text to a file """

        with open(p, 'w+', encoding=e) as file:
            file.write(d)

    def binary_writer(p, d):
        """ Writes out binaries to a file """

        with open(p, 'wb') as file:
            file.write(d)

    def pickle_writer(p, d):
        """ Writes out a pickled data serialized content in a file """

        with open(p, 'wb+') as file:
            pickle.dump(d, file, pickle.HIGHEST_PROTOCOL)

    def json_writer(p, d):
        """ Writes out a json data serialized content in a file """

        with open(p, 'w+') as file:
            json.dump(d, file)

    if fmt is 't':
        text_writer(path, data, encoding)
    elif fmt is 'b':
        binary_writer(path, data)
    elif fmt is 'p':
        pickle_writer(path, data)
    elif fmt is 'j':
        json_writer(path, data)
    else:
        raise ValueError("Format is not valid!\n")
