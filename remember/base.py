import hashlib
from functools import update_wrapper
from inspect import getfile
from itertools import chain
from os.path import isfile, join, dirname, basename, splitext


def file_backed_decorator_factory(cls):
    def decorator(filename_or_function=None, *args, **kwargs):
        # used without arguments, filename_or_function is a function
        if callable(filename_or_function) and not args and not kwargs:
            return cls(filename_or_function)

        # "partially applied" constructor
        def wrapper(function):
            return cls(function, filename_or_function, *args, **kwargs)

        return wrapper

    return decorator


class CachedCallable(object):
    def __init__(self, function, filename=None):
        self.function = function
        self.filename = filename

        # ensure that callable object looks like the function
        update_wrapper(self, function)

    def __call__(self, *args, **kwargs):
        filename = self.filename
        function = self.function

        # source path of wrapped function (cache file will be sibling)
        source_location = getfile(function)

        if filename is None:
            # generate hash of arguments
            argv = args + tuple(chain.from_iterable(kwargs.iteritems()))
            argh = hashlib.md5(''.join(map(str, argv))).hexdigest()

            # dynamically generated filename
            filename, _ = splitext(basename(source_location))
            filename += '_{}_{}.cache'.format(function.__name__, argh)
        else:
            # passed filename
            filename = filename.format(*args, **kwargs)

        # place in the same directory as calling function
        filepath = join(dirname(source_location), filename)

        # check and return cached result
        if isfile(filepath):
            return self.load(filepath)

        # compute and save result
        result = function(*args, **kwargs)
        saved = self.save(filepath, result)
        return result if saved is None else saved

    def now(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def load(self, filepath):
        raise NotImplementedError

    def save(self, filepath, result):
        raise NotImplementedError
