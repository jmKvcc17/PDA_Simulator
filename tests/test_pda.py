import unittest
from resources import pda
from resources import json_reader

class TestPDASimulator(unittest.TestCase):

    def test_string_acceptance(self):
        """
        Tests if a string is accepted or rejected by a DPA
        """
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
        self.assertFalse(test2.check_string("a"))
        self.assertTrue(test2.check_string("abba"))
        self.assertTrue(test2.check_string("abab"))
        self.assertTrue(test2.check_string("baba"))

        test3 = pda.PDA(json_reader.read_file(file_dir + 'pda_7_1_2.json'))
        self.assertTrue(test3.check_string(""))
        self.assertTrue(test3.check_string("a"))
        self.assertTrue(test3.check_string("ab"))
        self.assertTrue(test3.check_string("aaaaaaaaaa"))
        self.assertTrue(test3.check_string("aaaaaaabbbbbbb"))
        self.assertFalse(test3.check_string("aaaaaaabbbbbb"))
        self.assertFalse(test3.check_string("abba"))
        self.assertFalse(test3.check_string("abab"))
        self.assertFalse(test3.check_string("baba"))

    def test_string_in_alphabet(self):
        """
        Tests if a string contains only characters defined in the alphabet
        """
        file_dir = './files/'
        print()
        print("Testing if string contains characters defined in the alphabet.")

        test1 = pda.PDA(json_reader.read_file(file_dir + 'pda_1_edit.json'))
        self.assertTrue(test1.check_if_in_alphabet(""))
        self.assertTrue(test1.check_if_in_alphabet("0"))
        self.assertTrue(test1.check_if_in_alphabet("1"))
        self.assertTrue(test1.check_if_in_alphabet("00"))
        self.assertTrue(test1.check_if_in_alphabet("11"))
        self.assertFalse(test1.check_if_in_alphabet("a"))
        self.assertFalse(test1.check_if_in_alphabet("b"))
        self.assertFalse(test1.check_if_in_alphabet("a0011"))
        self.assertFalse(test1.check_if_in_alphabet("0011a"))



if __name__ == '__main__':
    unittest.main()