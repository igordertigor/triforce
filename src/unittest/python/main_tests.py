import unittest
import unittest.mock as mock

from triforce.main import Virtualenv, parse_venv


class TestVirtualEnv(unittest.TestCase):

    @mock.patch('triforce.main.DEFAULT_VENV_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.execute')
    def test_create_py3(self, execute_mock):
        venv = Virtualenv('ANY_VENV')
        venv.create()
        execute_mock.assert_called_once_with('pyvenv ANY_PREFIX/ANY_VENV')

    @mock.patch('triforce.main.DEFAULT_VENV_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.execute')
    def test_create_py2(self, execute_mock):
        venv = Virtualenv('ANY_VENV', venv_command='python2')
        venv.create()
        execute_mock.assert_called_once_with('virtualenv ANY_PREFIX/ANY_VENV')

    @mock.patch('triforce.main.DEFAULT_VENV_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.execute')
    def test_create_any_command(self, execute_mock):
        venv = Virtualenv('ANY_VENV', venv_command='ANY_COMMAND')
        venv.create()
        execute_mock.assert_called_once_with('ANY_COMMAND ANY_PREFIX/ANY_VENV')


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

    def test_parse_venv_triforce(self):
        input_ = {'triforce': {'venv_command': 'ANY_VENV_COMMAND',
                               'venv_prefix': 'ANY_VENV_PREFIX',
                               'symlink_prefix': 'ANY_SYMLINK_PREFIX',
                               'install': 'false'}}
        expected = Virtualenv('ANY_VENV',
                              venv_prefix='ANY_VENV_PREFIX',
                              venv_command='ANY_VENV_COMMAND',
                              urls=['triforce'],
                              symlink_prefix='ANY_SYMLINK_PREFIX',
                              symlinks=['triforce'],
                              )
        received = parse_venv('ANY_VENV', input_)
        self.assertEqual(expected, received)

    def test_parse_venv_triforce_no_install(self):
        input_ = {'triforce': {'venv_command': 'ANY_VENV_COMMAND',
                               'venv_prefix': 'ANY_VENV_PREFIX',
                               'symlink_prefix': 'ANY_SYMLINK_PREFIX'}}
        expected = Virtualenv('ANY_VENV',
                              venv_prefix='ANY_VENV_PREFIX',
                              venv_command='ANY_VENV_COMMAND',
                              symlink_prefix='ANY_SYMLINK_PREFIX',
                              )
        received = parse_venv('ANY_VENV', input_)
        self.assertEqual(expected, received)
