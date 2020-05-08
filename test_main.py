import unittest

class TestMain(unittest.TestCase):
    def setUp(self):
        print('setup')

    def tearDown(self):
        print('tearDown')

    def test_1(self):
        self.assertTrue(True)
