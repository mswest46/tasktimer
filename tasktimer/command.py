import pickle
from task import Task
from datetime import datetime
import subprocess
import sys
import os
from termcolor import colored, cprint
from . import get_data
import shutil


TASKS_FILE =  'tasks.pickle'

class Command(): 

    def __init__(self, filename = TASKS_FILE): 
        self.tasks = None
        if not os.path.isdir(get_data()): 
            os.mkdir(get_data())
            print("making data directory") 
        self.tasks_file = get_data() + filename
        self.load()

    def load(self): 
        try: 
            with open(self.tasks_file, 'r') as f: 
                self.tasks = pickle.load(f)
        except IOError: 
            self.tasks = [] 

    def save(self): 
        try: 
            with open(self.tasks_file, 'w+') as f: 
                pickle.dump(self.tasks, f)
        except: 
            raise

    def add(self, command_options): 
        data = extract_add_data(command_options, self.tasks)
        t = Task(data)
        self.tasks.insert(0, t)
        self.list(command_options)
        self.save()

    def list(self, command_options, out = False): 

        print("\033c")
        filterfun = extract_filter_data(command_options) 
        # terminal_width = int(subprocess.check_output(['tput', 'cols']))

        # which parts of task data should I display and in what order? 
        display_keys = ['number', 'description', 'estimate', 'due', 'status']

        # what should the column labels be? 
        column_names = {'number': 'NO.', 'description': 'TASK', 'estimate': 'ESTIMATE', 'due': 'DUE', 'status': 'STATUS'}

        # get the display string for each task for each column
        task_string_array = []
        color_array = []

        number_to_index = {}
        
        number = 1
        for i, t in enumerate(self.tasks): 
            if filterfun(t): 
                number_to_index[number] = i
                color_array.append(get_display_color(t, display_keys))
                t_strings = {}
                for key in display_keys: 
                    t_strings[key] = format_string(t, key, number)
                task_string_array.append(t_strings)
                number += 1


        # find the maximum length in each column (including column label)
        column_widths = {key: max(max([len(t_strings[key]) for t_strings in task_string_array]), len(column_names[key]))
                for key in display_keys}
        
        divider = " | " 

        # print column names
        string = divider
        for key in display_keys: 
            string += column_names[key].ljust(column_widths[key]) + divider 
        cprint(string, 'white', 'on_blue', attrs = ['bold'])

        for i, t_string in enumerate(task_string_array):
            string = divider
            for key in display_keys: 
                string += t_string[key].ljust(column_widths[key]) + divider
            cprint(string, color_array[i])

        if out: 
            return number_to_index 

    def move(self, command_options): 
        while True: 
            number_to_index = self.list(command_options, out = True)
            print("move from? Or hit enter to break")
            move_from = raw_input().lower()
            if move_from == "":
                break
            move_from = int(move_from)
            print("move to?")
            move_to = int(raw_input().lower())
            t = self.tasks.pop(number_to_index[move_from])
            self.tasks.insert(number_to_index[move_to],  t)
        self.save()

    def start(self, command_options, n = 0): 
        self.tasks[0].start()
        self.save()
        self.list(command_options)

    def finish(self, command_options, n = 0): 
        t = self.tasks.pop(0)
        t.finish()
        self.tasks.append(t)
        self.list(command_options)
        self.save()

    def delete(self, command_options, n = 0): 
        self.tasks.pop(0)
        self.save()

    def deleteall(self, command_options): 
        shutil.rmtree(get_data())


def format_string(t, key, number): 
    if key == 'number':
        return str(number)
    if key == 'due':
        d = t.get(key).day - datetime.now().day
        if d == 0: 
            return "today"
        elif d < 0: 
            return "overdue"
        else: 
            return "in {} days".format(d)
    if key == 'estimate': 
        return "{} hrs".format(t.get(key)) if t.get(key) else ""
    if key == 'status':
        display_status = {
                'pending': 'to do',
                'progress': 'doing',
                'complete': 'done'
                }
        return display_status[t.get('status')]

    return str(t.get(key)) if t.get(key) else ""

def get_display_color(t, display_keys): 

    # we're complete
    if ('status' in display_keys):
        if t.get('status') == 'complete':
            return 'blue'
        elif t.get('status') == 'progress': 
            return 'magenta'

    # we're overdue
    if ('due' in display_keys and 
            t.get('due').day < datetime.now().day):
        return 'red'

    return None
    
def extract_filter_data(command_options):
    def filterfun(task): 
        return task.get('due').day <= datetime.now().day

    #     return ((task.get('status') == 'pending' or 
    #             task.get('status') == 'progress') 
    #             and task.get('due').day <= datetime.now().day )
    return filterfun

def extract_add_data(options, tasks): 
    return {'ID': get_new_id(tasks),
            'description': options[DESCRIPTION_OPTION],
            'status': 'pending',
            'estimate': options[ESTIMATE_OPTION] if options[ESTIMATE_OPTION] else None, 
            'due': make_due_date(options[DUE_OPTION]) if options[DUE_OPTION] else make_due_date('today'), 
            'priority': options[PRIORITY_OPTION] if options[PRIORITY_OPTION] else None,
            'created': datetime.now()
            }
            
def get_new_id(tasks): 
    try: 
        return max([t.get('ID') for t in tasks])
    except ValueError:
        return 1
    
def make_due_date(string): 
    if string == 'today':
        midnight_today = datetime.now().replace(
                hour = 23, 
                minute = 59, 
                second = 59)
        return midnight_today
    return None

PRIORITY_OPTION = '--priority'
ESTIMATE_OPTION = '--estimate'
DESCRIPTION_OPTION = '<description>'
RECUR_OPTION = '--recur'
FILTER_OPTION = '--filter'
DUE_OPTION = '--due'
