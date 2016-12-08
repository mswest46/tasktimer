""" Packageing settings. """

from os.path import abspath, dirname, join
from setuptools import setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.txt') as file:
        long_description = fild.read()

# I have no idead what this is doing. testing or some shit. 
class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=tasktimer', '--cov-report=term-missing'])
        raise SystemExit(errno)

setup(name='tasktimer',
      version=__version__,
      description='A tasklist and timer',
      url='https://github.com/mswest46',
      author='Michael West',
      author_email='michael.singer.west@gmail.com',
      license='UNLICENSE',
      packages=['tasktimer'],
      zip_safe=False)

setup(
    name = 'skele',
    version = __version__,
    description = 'A skeleton command line program in Python.',
    long_description = long_description,
    url = 'https://github.com/rdegges/skele-cli',
    author = 'Randall Degges',
    author_email = 'r@rdegges.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'skele=skele.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
