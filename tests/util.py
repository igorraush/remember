class CacheTest(object):
    def teardown(self):
        import os

        # clean up cache files
        for item in os.listdir('.'):
            if os.path.isfile(item) and os.path.splitext(item)[1] == '.cache':
                os.remove(item)
