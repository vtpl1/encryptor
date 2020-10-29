import random
import tempfile
import unittest

from encryptor import folder_to_list

from . import utils


class TestFolderToList(unittest.TestCase):
    """
    docstring
    """
    def test_empty_param(self):
        self.assertRaises(TypeError, folder_to_list.get_list)

    def test_return_empty(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            print('created temporary directory', tmpdirname)
            for a in range(random.randint(1, 10)):
                utils.generate_big_random_bin_file(utils.generate_random_string(), 10*1024*1024)

            self.assertListEqual(folder_to_list.get_list(tmpdirname), [])
