import os.path as opath
import pickle


def check_path(path: str):

    if not opath.isfile(path):
        raise FileNotFoundError


def reader(path: str, mode: str):
    """ Wrapper for various methods to read data from a file

    :param path: path to the file
    :param mode: 't' for text file, 'b' for binary and 'p' for pickle
    :return: read content
    """

    def text_reader(p):
        """ Reads in all of a textual file """

        with open(p, 'r') as read:
            data = read.read()
        return data

    def binary_reader(p):
        """ Reads in all of a file in binaries """

        with open(p, 'rb') as read:
            data = read.read()
        return data

    def pickle_reader(p):
        with open(p, 'rb') as read:
            data = pickle.loads(read.read())
        return data

    check_path(path)

    if mode is 't':
        return text_reader(path)
    elif mode is 'b':
        return binary_reader(path)
    elif mode is 'p':
        return pickle_reader(path)


def writer(path: str, data, mode: str):
    """ Wrapper for various methods to write data to a file
    :param path: path to the file
    :param data: data to be writen in file
    :param mode: 't' for text file, 'b' for binary and 'p' for pickle
    """

    def text_writer(p, d):
        """ Writes out text to a file """

        with open(p, 'w+') as write:
            write.write(d)

    def binary_writer(p, d):
        """ Writes out binaries to a file """

        with open(p, 'wb') as write:
            write.write(d)

    def pickle_writer(p, d):
        """ Writes out a data serialized content in a file """

        with open(p, 'wb+') as write:
            pickle.dump(d, write, pickle.HIGHEST_PROTOCOL)

    check_path(path)

    if mode is 't':
        text_writer(path, data)
    elif mode is 'b':
        binary_writer(path, data)
    elif mode is 'p':
        pickle_writer(path, data)
