from json import load, dump

from .base import CachedCallable, file_backed_decorator_factory


class DictCachedCallable(CachedCallable):
    def load(self, filename):
        with open(filename, 'r') as fp:
            return load(fp)

    def save(self, filename, result):
        with open(filename, 'w') as fp:
            dump(result, fp)


dict = file_backed_decorator_factory(DictCachedCallable)
