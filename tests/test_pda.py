import unittest
from resources import pda
from resources import json_reader

class TestPDASimulator(unittest.TestCase):

    def test_string_acceptance(self):
        file_dir = './files/'

        test1 = pda.PDA(json_reader.read_file(file_dir + 'pda_1_edit.json'))

        self.assertTrue(test1.check_string(""))
        self.assertTrue(test1.check_string("0"))
        self.assertFalse(test1.check_string("1"))
        self.assertTrue(test1.check_string("00"))
        self.assertFalse(test1.check_string("11"))
        self.assertTrue(test1.check_string("0011"))
        self.assertFalse(test1.check_string("1110001"))
        self.assertFalse(test1.check_string("1111111"))
        self.assertTrue(test1.check_string("0000000"))

        test2 = pda.PDA(json_reader.read_file(file_dir + 'pda_7_2_2.json'))
        self.assertTrue(test2.check_string(""))
        self.assertTrue(test2.check_string("abba"))


if __name__ == '__main__':
    unittest.main()