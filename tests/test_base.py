import inspect
from nose.tools import *  # noqa

import remember
from remember.base import CachedCallable


class TestFileBackedDecorator(object):
    def test_basic_setup(self):
        @remember.dict
        def f():
            """
            This is used statically.
            """
            return 2

        @remember.dict()
        def g():
            """
            This is used without any arguments.
            """
            return 2

        ok_(isinstance(f, CachedCallable))
        eq_('f', f.__name__)
        eq_('This is used statically.', inspect.getdoc(f))

        ok_(isinstance(g, CachedCallable))
        eq_('g', g.__name__)
        eq_('This is used without any arguments.', inspect.getdoc(g))

    def test_immediate_invocation(self):
        @remember.dict
        def f(a=1):
            return a

        eq_(1, f.now())
        eq_(2, f.now(2))
        eq_(3, f.now(a=3))
