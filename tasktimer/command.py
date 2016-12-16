from __future__ import print_function
import pickle
from task import Task
from datetime import datetime
import subprocess
import sys
import os
from termcolor import colored, cprint
from . import get_data
import shutil
import timeutils


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
        # terminal_width = int(subprocess.check_output(['tput', 'cols']))

        # this little sequence pushes everything to the top of the terminal
        print("\033c")

        # filter
        filterfun = extract_filter_data(command_options) 

        # which parts of task data should I display and in what order? 
        column_keys = ['number', 'status', 'description', 'due', 'estimate', 'time_spent']

        row_content = []
        row_color = []

        # make colomn row
        column_names = {'number': 'NO.', 'description': 'TASK', 'estimate': 'ESTIMATE', 'due': 'DUE', 'status': 'STATUS', 'time_spent': 'TIME SPENT'}
        row_content.append([column_names[key] for key in column_keys])
        row_color.append([None for key in column_keys])

        # this loop determines the order in which tasks are displayed. So we note the number to index mapping as well as getting strings for each row and column
        number_to_index = {}
        n = 1
        div = None
        for i, t in enumerate(self.tasks): 
            if filterfun(t): 
                if not div and t.get('status') == 'complete': 
                    div = n
                number_to_index[n] = i
                row, color = get_row(t, column_keys, n)
                n += 1
                row_content.append(row)
                row_color.append(color)
        
        # make totals row
        total_row, total_color = get_total_row(self.tasks, filterfun, column_keys)
        row_content.append(total_row)
        row_color.append(total_color)

        # get widths of columns for printing 
        column_widths = [max([len(row[i]) for row in row_content]) for i in range(len(column_keys))]

        divider = " | "
        beginner = " "
        alt_divider = "   "

        # print column names
        string = beginner
        columns = row_content[0]
        for i in range(len(column_keys) - 1):
            string += columns[i].ljust(column_widths[i])
            string += divider
        string += columns[-1].ljust(column_widths[-1])
        string += beginner
        cprint(string, 'white', 'on_blue', attrs = ['bold'])

        # print tasks
        for i in range(1, len(row_content) - 1): 
            row = row_content[i]
            color = row_color[i]
            if i == div:
                # print dividing line
                l = sum(column_widths) + 3 * (len(column_widths) - 1)
                line = beginner + l * '_' + beginner
                print(line)
            print(beginner, end = "")
            for i in range(len(column_keys) - 1):
                cprint(row[i].ljust(column_widths[i]), color[i], end = "")
                print(divider, end = "")
            cprint(row[-1].ljust(column_widths[-1]), color[-1], end = "")
            print(beginner)

        # print dividing line
        l = sum(column_widths) + 3 * (len(column_widths) - 1)
        line = beginner + l * '_' + beginner
        print(line)

        # print totals
        string = beginner
        totals = row_content[-1]
        for i in range(len(column_keys) - 1):
            string += totals[i].ljust(column_widths[i])
            string += alt_divider
        string += row[-1].ljust(column_widths[-1])
        string += beginner
        cprint(string, 'white', attrs = ['bold'])
        
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
        self.list(command_options)
        self.save()

    def deleteall(self, command_options): 
        shutil.rmtree(get_data())

def get_row(t, display_keys, number): 
    """ outputs two arrays, one of strings to be displayed and one of colors (strings) for the corresponding to be displayed in"""
    row = []
    color = []
    for key in display_keys:
        if key == 'number': 
            row.append(str(number))
            color.append(None)
        elif key == 'due':
            d = t.get(key).day - datetime.now().day
            if d == 0: 
                string = "today"
                col = None 
            elif d < 0: 
                string = "overdue"
                col = 'red'
            else: 
                string = "in {} days".format(d)
                col = None
            row.append(string)
            color.append(col)
        elif key == 'description': 
            row.append(t.get('description'))
            display_color = {
                    'pending': None,
                    'progress': 'green',
                    'complete': None 
                    }
            color.append(display_color[t.get('status')])
        elif key == 'estimate':
            row.append(timeutils.timedelta2hourmin_string(t.get('estimate')))
            # row.append("{} hrs".format(t.get(key)) if t.get(key) else "")
            color.append(None)
        elif key == 'time_spent':
            if t.get_progress(): 
                time_spent_string = timeutils.timedelta2hourmin_string(
                        t.get_progress()
                        )
                col = 'red' if t.get_progress() > t.get('estimate') else 'green'
                # col = None
                row.append(time_spent_string)
                color.append(col)
            else:
                row.append("")
                color.append(None)
        elif key == 'status':
            display_status = {
                    'pending': 'to do',
                    'progress': 'doing',
                    'complete': 'done'
                    }
            row.append(display_status[t.get('status')])
            color.append(None)
        else: 
            row.append("")
            color.append(None)
    assert(len(row) == len(color))

    return row, color

def get_total_row(tasks, filterfun, display_keys):
    row = []
    color = []
    for key in display_keys: 
        if key == 'description': 
            row.append('TOTALS')
            color.append(None)
        elif key == 'estimate':
            # est_tot = str(sum(
            #         [float(t.get('estimate')) for t in tasks if filterfun(t)]
            #         ))
            est_tot = su
            est_tot = '10'
            row.append(est_tot)
            color.append(None)
        elif key == 'time_spent': 
            spent_tot = "{0:.1f}".format(sum(
                    [timeutils.timedelta2hour_float(t.get_progress()) for t in tasks 
                        if filterfun(t) and t.get_progress()]
                    ))
            row.append(spent_tot)
            color.append(None)
        else: 
            row.append("")
            color.append(None)
    assert(len(row) == len(color))
    return row, color

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
            # 'estimate': float(options[ESTIMATE_OPTION]) if options[ESTIMATE_OPTION] else None, 
            'estimate': timeutils.hour_string2time_delta(options[ESTIMATE_OPTION]) if options[ESTIMATE_OPTION] else None, 
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
