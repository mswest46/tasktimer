""" Packageing settings. """

from os.path import abspath, dirname, join
from setuptools import find_packages, setup
from tasktimer import __version__

def readme(): 
    this_dir = abspath(dirname(__file__))
    with open(join(this_dir, 'README.rst')) as file:
        return file.read()

setup(name='tasktimer',
      version = __version__,
      description='A tasklist and timer',
      long_description = readme(), 
      url='https://github.com/mswest46/tasktimer',
      author='Michael West',
      author_email='michael.singer.west@gmail.com',
      license='UNLICENSE',
      packages = find_packages(exclude=['docs', 'tests*']),
      install_requires = ['docopt', 'datetime', 'termcolor'], # dependencies 
      test_suite = 'nose.collector',
      tests_require = ['nose'], # nose is a testing thingamajig
      entry_points = {
          'console_scripts': [
              'task = tasktimer.cli:main'
          ]
      })
