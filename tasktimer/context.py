
from task import Task
from taskDB import TaskDB
from display import Display

class Context(): 
    def __init__(self): 
        self.taskDB = TaskDB()
        self.display = Display()
    def run_command(self, command_options):
        command_name = self.get_command_name(command_options)
        try: 
            command = getattr(self, command_name)
        except: 
            raise
        command()

    def get_command_name(self, command_options): 
        for name in command_options:
            if command_options[name]:
                return name
        raise "this should never happen"

    def add(self):
        t = Task.brand_new("Do dishes")
        self.taskDB.add(t)
    def list(self, command_options):

        self.display(command_options)
    def move(self, command_options):
        self.taskDB.move()
    def start(self, command_optoins): 
        n = 0
        t = self.taskDB.get_task(n)
        t.start()

    def finish(self, command_options):
        t = self.taskDB.get_task(n)
        t.finish()
