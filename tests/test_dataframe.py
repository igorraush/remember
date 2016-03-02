from nose.tools import *  # noqa

import remember
from .util import CacheTest


class TestDataFrameDecorator(CacheTest):
    def test_basic_setup(self):
        try:
            import pandas as pd
        except ImportError:
            return

        @remember.dataframe
        def one():
            return pd.DataFrame({
                'A': [1, 2, 3],
                'B': [4, 5, 6]
            })

        eq_(1, one().loc[0, 'A'])
        eq_(2, one().loc[1, 'A'])
        eq_(3, one().loc[2, 'A'])

    def test_extra_arguments(self):
        try:
            import pandas as pd
        except ImportError:
            return

        @remember.dataframe(parse_dates=['date'])
        def two():
            return pd.DataFrame({
                'date': pd.date_range('10/13/1992', freq='H', periods=10)
            })

        eq_(pd.Timestamp('1992-10-13 00:00:00'), two().loc[0, 'date'])
        eq_(pd.Timestamp('1992-10-13 01:00:00'), two().loc[1, 'date'])
        eq_(pd.Timestamp('1992-10-13 02:00:00'), two().loc[2, 'date'])
