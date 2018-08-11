import pickle


def reader(path, mode):
    """ Wrapper for various reading from file methods """

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

    if mode is 't':
        return text_reader(path)
    elif mode is 'b':
        return binary_reader(path)
    elif mode is 'p':
        return pickle_reader(path)


def writer(path, data, mode):
    """ Wrapper for various writing to file methods """

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

    if mode is 't':
        text_writer(path, data)
    elif mode is 'b':
        binary_writer(path, data)
    elif mode is 'p':
        pickle_writer(path, data)