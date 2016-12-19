from . import get_data
import shutil
import os
import pickle

tasktimer_file = get_data('tasktimer.pickle')

def load(): 
    """ load the tasktimer object from tasktimer_file """

    if not os.path.isdir(get_data()): 
        os.mkdir(get_data())
        print("making data directory") 
    try: 
        with open(tasktimer_file, 'r') as f: 
            return pickle.load(f)
    except IOError: 
        print("no tasktimer object in tasktimer_file")
        return None

def save(tasktimer): 
    """ save the tasktimer object to tasktimer_file """
    try: 
        with open(tasktimer_file, 'w+') as f: 
            pickle.dump(tasktimer, f)
    except: 
        raise

def delete_tasktimer_file(): 
    """ delete the data directory """
    shutil.rmtree(get_data())
