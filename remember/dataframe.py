from .base import CachedCallable, file_backed_decorator_factory

try:
    from pandas import read_csv
except ImportError:
    def read_csv(*args, **kwargs):  # noqa
        raise ImportError('pandas must be installed to use dataframe decorator')


class DataFrameCachedCallable(CachedCallable):
    def __init__(self, function, filename=None, **kwargs):
        self.kwargs = kwargs

        # parent init
        super(DataFrameCachedCallable, self).__init__(function, filename)

    def load(self, filename):
        return read_csv(filename, **self.kwargs)

    def save(self, filename, result):
        result.to_csv(filename, header=True, index=False)


dataframe = file_backed_decorator_factory(DataFrameCachedCallable)
