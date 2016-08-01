triforce - system virtualenv symlink manager
--------------------------------------------

This is a system virtualenv symlink manager. It allows you main so-called
system virtualenvironments that contain system utilities that you want to
install with pip but that should reside outside the virtualenvs that you are
using for development.  In fact, the use-case is similar to `pipsi
<https://github.com/mitsuhiko/pipsi>`_ but takes a somewhat different approach.
It was born out of my need to have a tool that suits exactly my needs. As such,
it is probably biased to my particular way of getting things done.

Principles
----------

* Declarative configuration based
* Configurable path for the virtualenvs and the symlinks
* Support one or many virtualenvs

Example
-------

Consider the following example.yaml:

.. code:: yaml

    .demo_sysvenv3:
        triforce:
            venv_prefix: /tmp/example
            symlink_prefix: /tmp/example
        ipython:
            symlink: ['ipython', 'iptest']
        yadoma: {}
    .demo_sysvenv2:
        triforce:
            venv_command: python2
            venv_prefix: /tmp/example
            symlink_prefix: /tmp/example
        git-spindle:
            url: git+ssh://git@github.com/seveas/git-spindle.git
            symlink: ['git-hub']

This will create two system virtualenvs `.demo_sysvenv3` and `.demo_sysvenv2`.
The first, is based on Python 3 (the default) and the second on legacy Python.
Each system virtualenv contains a number of packages that will be installed and
linked.

The special `triforce` section contains additional parameters that govern how
the system virtualenv will be configured. For example in both cases above, the
virtualenvs themselves and their symlinks will be installed into `/tmp/example`
(to ensure the example doesn't screw with your system). In the `.demo_sysvenv2`
case, the `venv_command` command has been set to `python2` indicating that a
virtualenv with legacy python should be installed. In case that command doesn't
work for you, you can also simply type a custom command string to create the
virtualenv for you. This is provided as a fallback since there seem to be a
myriad of ways of setting up a virtualenv and you never know what might work on
a given system.

In addition to the names of the programs on PyPi, you need to specify which
executables should be symlinked. This may seem redundant, but a) I don't know
how to easily introspect a Python package to obtain the scripts it installs and
b) maybe you want to have control over this. Anyway, for the tool `yadoma`
above there is no list of symlinks and so the tool will attempt to symlink a
script of the same name as the package on PyPi. Yes, this could have been done
for `ipython` too, but then we wouldn't link the `iptest` script. Lastly, you
can also specify a `url` which may contain the string that will be passed on to
`pip`. In the example above we install `git-spindle` from github.

Lastly, I should also note that the tools `pip` and `pybuilder` will be
installed by default into each created system virtualenv.

Here is what it looks like in action:

.. code::

    % ./triforce example.yaml                                                                                               :(
    {'path': '/tmp/example/.demo_sysvenv2', 'symlink_prefix': '/tmp/example', 'venv_prefix': '/tmp/example', 'name': '.demo_sysvenv2', 'symlinks': ['git-hub'], 'venv_command': 'python2', 'urls': ['git+ssh://git@github.com/seveas/git-spindle.git']}
    Creating venv at: '/tmp/example/.demo_sysvenv2'
    Running virtualenv with interpreter /usr/bin/python2
    New python executable in /tmp/example/.demo_sysvenv2/bin/python2
    Also creating executable in /tmp/example/.demo_sysvenv2/bin/python
    Installing setuptools, pkg_resources, pip, wheel...done.
    
    'pip' command is: '/tmp/example/.demo_sysvenv2/bin/pip'
    Installing/upgrading utilities: 'pip' and 'pybuilder'
    Requirement already up-to-date: pip in /tmp/example/.demo_sysvenv2/lib/python2.7/site-packages
    Collecting pybuilder
    Collecting tblib (from pybuilder)
      Using cached tblib-1.3.0-py2.py3-none-any.whl
    Requirement already up-to-date: wheel in /tmp/example/.demo_sysvenv2/lib/python2.7/site-packages (from pybuilder)
    Installing collected packages: tblib, pybuilder
    Successfully installed pybuilder-0.11.9 tblib-1.3.0
    
    Installing dependencies: '['git+ssh://git@github.com/seveas/git-spindle.git']'
    Collecting git+ssh://git@github.com/seveas/git-spindle.git
      Cloning ssh://git@github.com/seveas/git-spindle.git to /tmp/pip-uStkAq-build
    Collecting github3.py>=0.9.0 (from git-spindle==3.2)
      Using cached github3.py-0.9.5-py2.py3-none-any.whl
    Collecting whelk>=2.6 (from git-spindle==3.2)
    Collecting docopt>=0.5.0 (from git-spindle==3.2)
    Collecting uritemplate.py>=0.2.0 (from github3.py>=0.9.0->git-spindle==3.2)
    Collecting requests>=2.0 (from github3.py>=0.9.0->git-spindle==3.2)
      Using cached requests-2.10.0-py2.py3-none-any.whl
    Installing collected packages: uritemplate.py, requests, github3.py, whelk, docopt, git-spindle
      Running setup.py install for git-spindle ... done
    Successfully installed docopt-0.6.2 git-spindle-3.2 github3.py-0.9.5 requests-2.10.0 uritemplate.py-0.3.0 whelk-2.6
    
    Will symlink: '/tmp/example/.demo_sysvenv2/bin/git-hub' --> '/tmp/example/git-hub'
    {'path': '/tmp/example/.demo_sysvenv3', 'symlink_prefix': '/tmp/example', 'venv_prefix': '/tmp/example', 'name': '.demo_sysvenv3', 'symlinks': ['ipython', 'iptest', 'yadoma'], 'venv_command': 'python3', 'urls': ['ipython', 'yadoma']}
    Creating venv at: '/tmp/example/.demo_sysvenv3'
    
    'pip' command is: '/tmp/example/.demo_sysvenv3/bin/pip'
    Installing/upgrading utilities: 'pip' and 'pybuilder'
    Collecting pip
      Using cached pip-8.1.2-py2.py3-none-any.whl
    Collecting pybuilder
      Using cached PyBuilder-0.11.9.tar.gz
    Collecting tblib (from pybuilder)
      Using cached tblib-1.3.0-py2.py3-none-any.whl
    Collecting wheel (from pybuilder)
      Using cached wheel-0.29.0-py2.py3-none-any.whl
    Building wheels for collected packages: pybuilder
      Running setup.py bdist_wheel for pybuilder ... error
      Complete output from command /tmp/example/.demo_sysvenv3/bin/python3.5 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-xpca6850/pybuilder/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" bdist_wheel -d /tmp/tmpqkx5qndcpip-wheel- --python-tag cp35:
      usage: -c [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
         or: -c --help [cmd1 cmd2 ...]
         or: -c --help-commands
         or: -c cmd --help
      
      error: invalid command 'bdist_wheel'
      
      ----------------------------------------
      Running setup.py clean for pybuilder
    Failed to build pybuilder
    Installing collected packages: pip, tblib, wheel, pybuilder
      Found existing installation: pip 8.1.1
        Uninstalling pip-8.1.1:
          Successfully uninstalled pip-8.1.1
      Running setup.py install for pybuilder ... done
    Successfully installed pip-8.1.2 pybuilder-0.11.9 tblib-1.3.0 wheel-0.29.0
    
    Installing dependencies: '['ipython', 'yadoma']'
    Collecting ipython
      Using cached ipython-5.0.0-py2.py3-none-any.whl
    Collecting yadoma
    Collecting pexpect; sys_platform != "win32" (from ipython)
      Using cached pexpect-4.2.0-py2.py3-none-any.whl
    Collecting prompt-toolkit<2.0.0,>=1.0.3 (from ipython)
      Using cached prompt_toolkit-1.0.3-py3-none-any.whl
    Collecting pickleshare (from ipython)
      Using cached pickleshare-0.7.3-py2.py3-none-any.whl
    Collecting pygments (from ipython)
      Using cached Pygments-2.1.3-py2.py3-none-any.whl
    Collecting decorator (from ipython)
      Using cached decorator-4.0.10-py2.py3-none-any.whl
    Collecting traitlets>=4.2 (from ipython)
      Using cached traitlets-4.2.2-py2.py3-none-any.whl
    Requirement already satisfied (use --upgrade to upgrade): setuptools>=18.5 in /tmp/example/.demo_sysvenv3/lib/python3.5/site-packages (from ipython)
    Collecting simplegeneric>0.8 (from ipython)
    Collecting docopt (from yadoma)
    Collecting pyyaml (from yadoma)
    Collecting ptyprocess>=0.5 (from pexpect; sys_platform != "win32"->ipython)
      Using cached ptyprocess-0.5.1-py2.py3-none-any.whl
    Collecting six>=1.9.0 (from prompt-toolkit<2.0.0,>=1.0.3->ipython)
      Using cached six-1.10.0-py2.py3-none-any.whl
    Collecting wcwidth (from prompt-toolkit<2.0.0,>=1.0.3->ipython)
      Using cached wcwidth-0.1.7-py2.py3-none-any.whl
    Collecting ipython-genutils (from traitlets>=4.2->ipython)
      Using cached ipython_genutils-0.1.0-py2.py3-none-any.whl
    Installing collected packages: ptyprocess, pexpect, six, wcwidth, prompt-toolkit, pickleshare, pygments, decorator, ipython-genutils, traitlets, simplegeneric, ipython, docopt, pyyaml, yadoma
    Successfully installed decorator-4.0.10 docopt-0.6.2 ipython-5.0.0 ipython-genutils-0.1.0 pexpect-4.2.0 pickleshare-0.7.3 prompt-toolkit-1.0.3 ptyprocess-0.5.1 pygments-2.1.3 pyyaml-3.11 simplegeneric-0.8.1 six-1.10.0 traitlets-4.2.2 wcwidth-0.1.7 yadoma-41.3
    
    Will symlink: '/tmp/example/.demo_sysvenv3/bin/ipython' --> '/tmp/example/ipython'
    Will symlink: '/tmp/example/.demo_sysvenv3/bin/iptest' --> '/tmp/example/iptest'
    Will symlink: '/tmp/example/.demo_sysvenv3/bin/yadoma' --> '/tmp/example/yadoma'


TODO and Ideas
--------------

Many.


License
-------


Copyright 2016 Valentin Haenel <valentin@haenel.co>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
