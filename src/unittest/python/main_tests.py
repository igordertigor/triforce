import unittest

from triforce import Virtualenv, parse_venv


class TestParseVirtualEnv(unittest.TestCase):

    def test_parse_venv(self):
        input_ = {'ANY_PROGRAM': {}}
        expected = Virtualenv('ANY_VENV',
                              urls=['ANY_PROGRAM'],
                              symlinks=['ANY_PROGRAM'])
        received = parse_venv('ANY_VENV', input_)
        self.assertEqual(expected, received)

    def test_parse_venv_url(self):
        input_ = {'ANY_PROGRAM': {'url': 'ANY_URL'}}
        expected = Virtualenv('ANY_VENV',
                              urls=['ANY_URL'],
                              symlinks=['ANY_PROGRAM'])
        received = parse_venv('ANY_VENV', input_)
        self.assertEqual(expected, received)

    def test_parse_venv_symlinks(self):
        input_ = {'ANY_PROGRAM': {'symlink': ['ANY_SYMLINK',
                                              'ANOTHER_SYMLINK']}}
        expected = Virtualenv('ANY_VENV',
                              urls=['ANY_PROGRAM'],
                              symlinks=['ANY_SYMLINK', 'ANOTHER_SYMLINK'])
        received = parse_venv('ANY_VENV', input_)
        self.assertEqual(expected, received)
