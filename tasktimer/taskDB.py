import json
from task import Task

class TaskDB():
    def __init__(self):
        self.data = 0
        self.task_list = self.load_task_list() 

    def load_task_list(self): 
        try:
            with open('tasktimer/tasklist.json', 'r') as f:
                try: 
                    data = json.load(f)
                except ValueError: 
                    data = []
        except IOError:
            f = open('tasktimer/tasklist.json', 'w')
            f.close()
            data = []

        task_list = []
        for datum in data:
            t = Task(datum)
            task_list.append(t)
        print('task_list', task_list)
        return task_list

    def save_task_list(self): 
        try:
            with open('tasktimer/tasklist.json', 'w') as f: 
                json.dump([t.get_data() for t in self.task_list], f)
        except IOError:
            f = open('tasktimer/tasklist.json', 'w')
            json.dump([t.get_data() for t in self.task_list], f)
            f.close()


    def add(self, task): 
        self.task_list.append(task)
        self.save_task_list()

    def deleteDB(self, task): 
        os.remove('tasktimer/tasklist.json')

    


