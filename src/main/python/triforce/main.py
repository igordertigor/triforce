import os
import sys
import shlex

import sh
import yaml

DEFAULT_VENV_PREFIX = os.environ['HOME']
DEFAULT_VENV_COMMAND = "python3"
DEFAULT_SYMLINK_PREFIX = os.path.join(os.environ['HOME'], 'bin')


class Virtualenv(object):

    def __init__(self, name,
                 venv_prefix=None,
                 venv_command=None,
                 urls=None,
                 symlink_prefix=None,
                 symlinks=None):
        self.name = name
        self.venv_prefix = venv_prefix or DEFAULT_VENV_PREFIX
        self.path = os.path.join(self.venv_prefix, self.name)
        self.venv_command = venv_command or DEFAULT_VENV_COMMAND
        self.urls = urls or []
        self.symlink_prefix = symlink_prefix or DEFAULT_SYMLINK_PREFIX
        self.symlinks = symlinks or []

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (self.name == other.name and
                self.venv_prefix == other.venv_prefix and
                self.venv_command == other.venv_command and
                self.urls == other.urls and
                self.symlink_prefix == other.symlink_prefix and
                self.symlinks == other.symlinks
                )

    def create(self):
        print("Creating venv at: '{0}'".format(self.path))
        if self.venv_command in [2, '2', 'py2', 'python2']:
            print(self.execute('virtualenv {0}'.format(self.path)))
        elif self.venv_command in [3, '3', 'py3', 'python3']:
            print(self.execute('pyvenv {0}'.format(self.path)))
        else:
            print(self.execute('{0} {1}'.format(self.venv_command, self.path)))
        print("'pip' command is: '{0}'".format(self.pip_path))

    def bootstrap_utilities(self):
        print("Installing/upgrading utilities: 'pip' and 'pybuilder'")
        self.pip_install('pip')
        self.pip_install('pybuilder')

    @property
    def bin_path(self):
        return os.path.join(self.path, 'bin')

    @property
    def pip_path(self):
        return os.path.join(self.bin_path, 'pip')

    def pip_install(self, stuff):
        print(self.execute("{0} install -U {1}".
              format(self.pip_path, stuff), add_path=True))

    def install_dependencies(self):
        urls_string = ' '.join(self.urls)
        print("Installing dependencies: '{0}'".format(self.urls))
        self.pip_install(urls_string)

    def symlink(self):
        for link in self.symlinks:  # triforce... link...
            source = os.path.join(self.bin_path, link)
            target = os.path.join(self.symlink_prefix, link)
            print("Will symlink: '{0}' --> '{1}'".format(source, target))
            try:
                os.symlink(source, target)
            except FileExistsError:
                pass

    def process(self):
        self.create()
        self.bootstrap_utilities()
        self.install_dependencies()
        self.symlink()

    def execute(self, command, add_path=False):
        p = shlex.split(command)
        c = sh.Command(p[0])
        if not add_path:
            return c(p[1:])
        else:
            env = os.environ.copy()
            env['PATH'] = self.bin_path + ':' + env['PATH']
            return c(p[1:], _env=env)


def parse_venv(name, venv):
    venv_command, venv_prefix, symlink_prefix = None, None, None
    urls, symlinks = [], []
    for program, options in venv.items():
        if program == 'triforce':
                venv_command = options.get('venv_command')
                venv_prefix = options.get('venv_prefix')
                symlink_prefix = options.get('symlink_prefix')
                if 'install' in options:
                    urls.append('triforce')
                    symlinks.append('triforce')
        else:
            try:
                urls.append(options['url'])
            except KeyError:
                urls.append(program)
            try:
                symlinks.extend(options['symlink'])
            except KeyError:
                symlinks.append(program)

    return Virtualenv(name,
                      venv_prefix=venv_prefix,
                      venv_command=venv_command,
                      urls=urls,
                      symlink_prefix=symlink_prefix,
                      symlinks=symlinks)


def process_venvs(config_files):
    venvs = []
    for config_file in config_files:
        with open(config_file) as config_file_pointer:
            config = yaml.load(config_file_pointer)
            for name, venv in config.items():
                venvs.append(parse_venv(name, venv))
    return venvs


def entry():
    config_files = sys.argv[1:]
    try:
        for venv in process_venvs(config_files):
            print(venv)
            venv.process()
    except sh.ErrorReturnCode as e:
        print(e)
        print(e.stdout)
        print(e.stderr)
