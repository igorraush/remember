import inspect
from nose.tools import *  # noqa

import remember
from remember.base import CachedCallable


def issibling(name):
    from os.path import join, isfile, dirname
    return isfile(join(dirname(__file__), name))


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

    def test_default_filename(self):
        @remember.dict
        def f(a=1):
            return a

        f()
        ok_(issibling('test_base_f_d41d8cd98f00b204e9800998ecf8427e.cache'))

        f(2)
        ok_(issibling('test_base_f_d41d8cd98f00b204e9800998ecf8427e.cache'))

    def test_custom_filename(self):
        @remember.dict('{}_{}.cache')
        def f(a, b):
            return [a, b]

        eq_([1, 2], f(1, 2))
        ok_(issibling('1_2.cache'))
