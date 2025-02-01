import unittest
import bakesite.compile as compile


class TruncateTest(unittest.TestCase):
    def test_truncate(self):
        long_text = '  \n'.join('word' + str(i) for i in range(50))
        expected_text = ' '.join('word' + str(i) for i in range(25))
        self.assertEqual(compile.truncate(long_text), expected_text)
