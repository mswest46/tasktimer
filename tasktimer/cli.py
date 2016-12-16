"""tasktimer
 
Usage:
  task
  task add <description> --estimate <estimate> [--priority <priority>] [--recur <recur>] [--due <due>]
  task list [--filter <filter>]
  task move
  task start [--id <number>]
  task finish [--id <number>]
  task edit [--number <number>]
  task delete [--number <number>]
  task deleteall
  task -h | --help
  task --version
 
Options:
  -p <priority> --priority <priority>        the priority of new task 
  -e <estimate> --estimate <estimate>        the user's estimate of time to complete task
  -r <recur> --recur <recur>                 the recurring pattern of task (e.g. every hour)
  -d <due> --due <due>                       the due date of the task
  -f <filter> --filter <filter>              filter of list. (e.g. weeek) defaults to only showing today's tasks
  -id <number>                               the number (as shown by list) of the task the user is acting on
  -h --help                                  Show this screen.
  --version                                  Show version.
 
Examples:
  task hello
 
Help:

"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from command import Command
import pdb
import sys


def main():
    # options is a dict with keys = names of options as listed in Usage: docstring, options[name] = whether main was called with option 'name'
    options = docopt(__doc__)
    #TODO: use Schema package to validate all options passed in? Or validate within context object? Think about it.
    # Now, we make sense of the command options here, try to understand what the user is trying to say, and then 
    # call the command object
    command = Command()
    for name in options:
        if options[name] == True:
            com = getattr(command, name)
            break
    # TODO: pass in nicer version of command options maybe
    com(options)

