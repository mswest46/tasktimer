"""
tasktimer
 
Usage:
  task add
  task list
  task move
  task start
  task finish
  task -h | --help
  task --version
 
Options:
  -h --help                         Show this screen.
  --version                         Show version.
 
Examples:
  task hello
 
Help:

"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from context import Context
import pdb

def main():
    context = Context()

    # options is a dict with keys = names of options as listed in Usage: docstring, docopt[name] = whether main was called with option 'name'
    options = docopt(__doc__)
    # let context take care of making sense out of options
    context.run_command(options)



    #import commands
   # for com, val in options.iteritems(): # loop through CLI options
   #     if hasattr(commands, com) and val: # if there is an actual module in commands with name com and task called with this command
   #         module = getattr(commands, com) # get that module
   #         commands = getmembers(module, isclass) # a list of (name, value) pairs of classes in module 
   #         print('COMMANDS:', commands)
   #         command = [command[1] for command in commands if command[0] != 'Base'][0] # as long as its not named 'Base', returns the class
   #         command = command(options)
   #         command.run() # run it

