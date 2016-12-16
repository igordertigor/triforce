import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

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

    @mock.patch('triforce.main.Virtualenv.pip_install')
    def test_bootstrap_utilities(self, pip_install_mock):
        venv = Virtualenv('ANY_VENV')
        venv.bootstrap_utilities()
        pip_install_mock.assert_has_calls([mock.call('pip'),
                                           mock.call('pybuilder')])

    @mock.patch('triforce.main.DEFAULT_VENV_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.execute')
    def test_pip_install(self, execute_mock):
        venv = Virtualenv('ANY_VENV')
        venv.pip_install('ANY_PROGRAM')
        execute_mock.assert_called_once_with(
            'ANY_PREFIX/ANY_VENV/bin/pip install -U ANY_PROGRAM',
            add_path=True)

    @mock.patch('triforce.main.Virtualenv.pip_install')
    def test_install_dependencies(self, pip_install_mock):
        venv = Virtualenv('ANY_VENV', urls=['ANY_URL'])
        venv.install_dependencies()
        pip_install_mock.assert_has_calls([mock.call('ANY_URL')])

    @mock.patch('triforce.main.Virtualenv.pip_install')
    def test_install_dependencies_multiple(self, pip_install_mock):
        venv = Virtualenv('ANY_VENV', urls=['ANY_URL1', 'ANY_URL2'])
        venv.install_dependencies()
        pip_install_mock.assert_has_calls([mock.call('ANY_URL1 ANY_URL2')])

    @mock.patch('triforce.main.DEFAULT_SYMLINK_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.bin_path', 'ANY_BIN_PATH')
    def test_symlink(self):
        venv = Virtualenv('ANY_VENV', symlinks=['ANY_URL1'])
        with mock.patch('os.path.join') as join_mock:
            join_mock.side_effect = ['ANY_SOURCE', 'ANY_TARGET']
            with mock.patch('os.symlink') as symlink_mock:
                venv.symlink()
        join_mock.assert_has_calls([mock.call('ANY_BIN_PATH', 'ANY_URL1'),
                                    mock.call('ANY_PREFIX', 'ANY_URL1')])
        symlink_mock.assert_has_calls([mock.call('ANY_SOURCE', 'ANY_TARGET')])

    @mock.patch('triforce.main.DEFAULT_SYMLINK_PREFIX', 'ANY_PREFIX')
    @mock.patch('triforce.main.Virtualenv.bin_path', 'ANY_BIN_PATH')
    def test_symlink_fail(self):
        venv = Virtualenv('ANY_VENV', symlinks=['ANY_URL1'])
        with mock.patch('os.path.join') as join_mock:
            join_mock.side_effect = ['ANY_SOURCE', 'ANY_TARGET']
            with mock.patch('os.symlink') as symlink_mock:
                symlink_mock.side_effect = FileExistsError
                venv.symlink()

    @mock.patch('triforce.main.Virtualenv.create')
    @mock.patch('triforce.main.Virtualenv.bootstrap_utilities')
    @mock.patch('triforce.main.Virtualenv.install_dependencies')
    @mock.patch('triforce.main.Virtualenv.symlink')
    def test_process(self,
                     create_mock,
                     bootstrap_utilities_mock,
                     install_dependencies_mock,
                     symlink_mock,
                     ):
        venv = Virtualenv('ANY_VENV', symlinks=['ANY_URL1'])
        venv.process()
        create_mock.assert_called_once_with()
        bootstrap_utilities_mock.assert_called_once_with()
        install_dependencies_mock.assert_called_once_with()
        symlink_mock.assert_called_once_with()


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
