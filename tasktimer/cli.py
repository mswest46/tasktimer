"""
tasktimer
 
Usage:
  task add <description> [--priority <priority>] [--estimate <estimate>] [--recur <recur>] 
  task list [--filter <filter>]
  task move
  task start [--number <number>]
  task finish [--number <number>]
  task edit [--number <number>]
  task -h | --help
  task --version
 
Options:
  -p <priority> --priority <priority>        the priority of new task 
  -e <estimate> --estimate <estimate>        the user's estimate of time to complete task
  -r <recur> --recur <recur>                 the recurring pattern of task (e.g. every hour)
  -f <filter> --filter <filter>              filter of list. (e.g. weeek) defaults to only showing today's tasks
  -n <number> --number <number>              the number (as shown by list) of the task the user is acting on
  -h --help                                  Show this screen.
  --version                                  Show version.
 
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
    #TODO: use Schema package to validate all options passed in? Or validate within context object? Think about it.
    # let context take care of making sense out of options
    context.run_command(options)
