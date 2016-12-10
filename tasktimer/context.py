
from task import Task
from taskDB import TaskDB
from display import Display

priority_str = '--priority'
estimate_str = '--estimate'
description_str = '<description>'
recur_str = '--recur'
filter_str = '--filter'

class Context(): 
    """ This is the controller class. All serious logic should be delegated """

    def __init__(self): 
        self.taskDB = TaskDB()
        self.display = Display()
        self.command_options = None

    def run_command(self, command_options):
        command_name = self.get_command_name(command_options)
        try: 
            command = getattr(self, command_name)
        except: 
            raise
        self.command_options = command_options
        command()

    def get_command_name(self, command_options): 
        for name in command_options:
            if command_options[name] == True:
                return name
        raise "this should never happen"

    def add(self):
        print("COMMAND_OPTIONS")
        print(self.command_options)
        ID = self.taskDB.get_new_id()
        if self.command_options[priority_str]:
            priority = int(self.command_options[priority_str])
        else: 
            priority = self.taskDB.get_new_priority()
        if self.command_options[estimate_str]:
            estimate = float(self.command_options[estimate_str])
        else:
            estimate = None
        if self.command_options[recur_str]:
            recur = self.command_options[recur_str]
        assert(description_str in self.command_options)
        description = self.command_options[description_str]

        t = Task.brand_new(
                ID = ID, 
                description = description,
                priority = priority,
                estimate = estimate
                )
        self.taskDB.add(t)

    def list(self):
        if self.command_options[filter_str]:
            filt = self.command_options[filter_str]
        else:
            filt = 'today'
        tasks = self.taskDB.get_tasks(filt)
        self.display.show(tasks)

    def move(self, command_options):
        self.taskDB.move()
        self.display.show()

    def start(self, command_optoins): 
        n = 0
        t = self.taskDB.get_task(n)
        t.start()

    def finish(self, command_options):
        t = self.taskDB.get_task(n)
        t.finish()
