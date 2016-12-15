from unittest import TestCase
import tasktimer.cli as cli
from nose.tools import assert_equals, assert_raises
from docopt import docopt

doc = cli.__doc__

class TestDocOptAdd(TestCase):

    def test_add_description(self): 
        args = docopt(doc, ['add', 'test_desc'])
        assert_equals(args['add'], True)
        assert_equals(args['<description>'], 'test_desc')
        for arg in args:
            if arg not in ['add', '<description>']:
                assert not args[arg]

    def test_add_no_description(self): 
        # this is as workaround because I don't know what error docopt is raising
        errored = False
        try:
            args = docopt(doc, ['add'])
        except:
            errored = True
        assert(errored)

    def test_add_priority_1(self): 
        args = docopt(doc, ['add', 'test_desc', '--priority', '1'])
        assert_equals(args['--priority'], '1')

    def test_add_priority_2(self): 
        args = docopt(doc, ['add', 'test_desc', '-p', '1'])
        assert_equals(args['--priority'], '1')
        
    def test_add_recur_1(self): 
        args = docopt(doc, ['add', 'test_desc', '--recur', 'today'])
        assert_equals(args['--recur'], 'today')
        
    def test_add_recur_2(self): 
        args = docopt(doc, ['add', 'test_desc', '-r', 'today'])
        assert_equals(args['--recur'], 'today')

    def test_add_esimate_1(self): 
        args = docopt(doc, ['add', 'test_desc', '--estimate', "one hour"])
        assert_equals(args['--estimate'], 'one hour')

    def test_add_esimate_2(self): 
        args = docopt(doc, ['add', 'test_desc', '-e', "one hour"])
        assert_equals(args['--estimate'], 'one hour')

    """ make sure that nothing besides these options get called. """
    def test_add_all_options_1(self): 
        args = docopt(doc, ['add', 'test_desc', '--recur', 'today', '--priority', '1', '--estimate', "one hour"])
        assert_equals(args['--estimate'], 'one hour')
        assert_equals(args['--recur'], 'today')
        assert_equals(args['--priority'], '1')
        for key in args: 
            if key not in ['add', '<description>', '--estimate', '--recur', '--priority']:
                assert not args[key], key
        
        
class TestDocOptList(TestCase):

    def test_list(self): 
        args = docopt(doc, ['list'])
        assert_equals(args['list'], True)
        for arg in args:
            if arg != 'list':
                assert(not args[arg])
    
    def test_list_filter(self): 
        args = docopt(doc, ['list', '--filter', 'filt'])
        assert_equals(args['--filter'], 'filt')

