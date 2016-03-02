from nose.tools import *  # noqa

import remember
from .util import CacheTest


class TestDictDecorator(CacheTest):
    def test_basic_setup(self):
        @remember.dict
        def one(a=1):
            return a

        eq_(1, one())
        eq_(2, one(2))
        eq_(2, one(2))

        @remember.dict
        def two(a=1):
            return {'a': a}

        eq_(1, two()['a'])
        eq_(2, two(2)['a'])
        eq_(2, two(2)['a'])
