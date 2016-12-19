from __future__ import print_function
import pickle
from task import Task
from datetime import datetime, timedelta
import subprocess
import sys
import os
from termcolor import colored, cprint
from . import get_data
import shutil
import timeutils


class Tasktimer(): 

    def __init__(self): 
        self.maxID = 0
        self.tasks = []
        self.number_to_index = None
        self.insert_index = None
        self.filterfun = default_filter

    def unpickle(self): 
        """ call this every time we reload tasktimer. (temporary, only because I keep making changes and I 
        need to keep up to date) """
        self.get_insert_index() 

    def get_insert_index(self): 
        for i, t in enumerate(self.tasks): 
            if t.get('status') == 'complete':
                self.insert_index = i
                break

    def add(self, command_options): 
        data = extract_add_data(command_options, self.tasks)
        t = Task(data)
        self.tasks.insert(self.insert_index, t)
        self.insert_index += 1
        self.list()

    def move(self, command_options): 
        while True: 
            self.list()
            print("move from? Or hit enter to break")
            move_from = raw_input().lower()
            if move_from == "":
                break
            move_from = int(move_from)
            print("move to?")
            move_to = int(raw_input().lower())

            t = self.tasks.pop(self.number_to_index[move_from])
            self.tasks.insert(self.number_to_index[move_to],  t)

    def start(self, command_options): 
        n = int(command_options[NUMBER_OPTION])
        i = self.number_to_index[n]
        self.tasks[i].start()
        self.list()

    def finish(self, command_options): 
        n = int(command_options[NUMBER_OPTION])
        i = self.number_to_index[n]
        t = self.tasks.pop(i)
        t.finish()
        self.tasks.append(t)
        self.insert_index -= 1
        self.list()

    def next(self, command_options): 
        """ finish a task and start the task at the top of your list"""
        n = int(command_options[NUMBER_OPTION])
        i = self.number_to_index[n]
        t = self.tasks.pop(i)
        t.finish()
        self.tasks[0].start()
        self.tasks.append(t)
        self.insert_index -= 1
        self.list()


    def delete(self, command_options): 
        n = int(command_options[NUMBER_OPTION])
        i = self.number_to_index[n]
        self.tasks.pop(i)
        self.list()

    def postpone(self, command_options): 
        n = int(command_options[NUMBER_OPTION])
        i = self.number_to_index[n]
        self.tasks[i].postpone()
        self.list()

    def extract_filterfun(self, command_options): 
        return default_filter

    def list(self, command_options = None, out = False): 

        if not self.tasks: 
            print("No tasks in list, nothing to show")
            return

        if command_options: 
            self.filterfun = self.extract_filterfun(command_options) 

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
        self.div = None
        for i, t in enumerate(self.tasks): 
            if self.filterfun(t): 
                if not self.div and t.get('status') == 'complete': 
                    self.div = n
                number_to_index[n] = i
                row, color = get_row(t, column_keys, n)
                n += 1
                row_content.append(row)
                row_color.append(color)

        self.number_to_index = number_to_index

        # make totals row
        total_row, total_color = get_total_row(self.tasks, self.filterfun, column_keys)
        row_content.append(total_row)
        row_color.append(total_color)

        self.print_list(row_content, row_color)

    def print_list(self, row_content, row_color):
        n_row = len(row_content)
        n_columns = len(row_content[0])

        # width of current terminal
        term_width = int(subprocess.check_output(['tput', 'cols']))

        # get widths of columns for printing 
        widths = [max([len(row[i]) for row in row_content]) for i in range(n_columns)]

        header_row, header_color = row_content[0], row_color[0]
        task_rows, task_colors = row_content[1:-1], row_color[1:-1]
        footer_row, footer_color = row_content[-1], row_color[-1]

        dividers = {
                'div' : ' | ',
                'space_div' : '   ',
                'begin' : ' ',
                'end' : ' '
                }

        # this little sequence pushes everything to the top of the terminal
        print("\033c")

        self.print_header(header_row, header_color, widths, term_width, dividers)
        self.print_tasks(task_rows, task_colors, widths, term_width, dividers)
        self.print_divider(widths, term_width, dividers)
        self.print_footer(footer_row, footer_color, widths, term_width, dividers)

    def print_header(self, row, color, widths, term_width, dividers):
        n_columns = len(row)
        # print column names
        string = dividers['begin'] 
        for i in range(n_columns - 1):
            string += row[i].ljust(widths[i])
            string += dividers['div']
        string += row[-1].ljust(widths[-1])
        string += dividers['end'] 
        cprint(string, 'white', 'on_blue', attrs = ['bold'])
    
    def print_tasks(self, rows, colors, widths, term_width, dividers):
        # print tasks
        for i in range(len(rows)): 
            row = rows[i]
            color = colors[i]
            if i + 1 == self.div:
                self.print_divider(widths, term_width, dividers)
            # print row
            print(dividers['begin'], end = "")
            for i in range(len(widths) - 1):
                cprint(row[i].ljust(widths[i]), color[i], end = "")
                print(dividers['div'], end = "")
            cprint(row[-1].ljust(widths[-1]), color[-1], end = "")
            print(dividers['end'])

    def print_footer(self, row, color, widths, term_width, dividers):
        n_columns = len(row)
        # print column names
        string = dividers['begin'] 
        for i in range(n_columns - 1):
            string += row[i].ljust(widths[i])
            string += dividers['space_div']
        string += row[-1].ljust(widths[-1])
        string += dividers['end'] 
        cprint(string, 'white', attrs = ['bold'])

    def print_divider(self, widths, term_width, dividers):
        n_columns = len(widths)
        l = sum(widths) + len(dividers['div']) * (n_columns - 1)
        line = dividers['begin'] + l * '_' + dividers['begin']
        print(line)

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
                    'progress': 'blue',
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
            display_color = {
                    'pending': None,
                    'progress': 'blue',
                    'complete': None 
                    }
            row.append(display_status[t.get('status')])
            color.append(display_color[t.get('status')])
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
            td = timedelta()
            for t in tasks:
                if filterfun(t): 
                    td += t.get('estimate')
            est_tot = timeutils.timedelta2hourmin_string(td)
            row.append(est_tot)
            color.append(None)
        elif key == 'time_spent': 
            td = timedelta()
            for t in tasks: 
                if filterfun(t) and t.get_progress(): 
                    td += t.get_progress()
            spent_tot = timeutils.timedelta2hourmin_string(td)


#            spent_tot = "{0:.1f}".format(sum(
#                    [timeutils.timedelta2hour_float(t.get_progress()) for t in tasks 
#                        if filterfun(t) and t.get_progress()]
#                    ))
            row.append(spent_tot)
            color.append(None)
        else: 
            row.append("")
            color.append(None)
    assert(len(row) == len(color))
    return row, color

def default_filter(task): 
    return True
    # tasks that have been completed today
    complete = (task.get('status') == 'complete' and task.get('end_time').day == datetime.now().day)
    # tasks that are incomplete but are due today or overdue
    incomplete = (task.get('status') == 'incomplete' and task.get('due').day < datetime.now().day)
    return complete or incomplete

def extract_filter_data(command_options):
    def filterfun(task): 
        # my normal use case is show tasks completed tasks only if they've been done today and show incomplete 
        # tasks only if they're due today or earlier.
        complete = task.get('status') == 'complete' and task.get('end_time').day == datetime.now().day
        incomplete = task.get('status') == 'incomplete' and task.get('due').day < datetime.now().day
        return True
        return complete or incomplete

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
    except (ValueError, TypeError):
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
NUMBER_OPTION = '--number'
ESTIMATE_OPTION = '--estimate'
DESCRIPTION_OPTION = '<description>'
RECUR_OPTION = '--recur'
FILTER_OPTION = '--filter'
DUE_OPTION = '--due'
