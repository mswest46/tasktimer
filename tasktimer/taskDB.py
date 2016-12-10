import json
from task import Task
from constants import TASKFILE

class TaskDB():

    #TODO: change task list into dict with id keys and add meta data and have multiple databases for different statuses
    def __init__(self):
        self.data = 0
        self.task_list = self.load_task_list() 

    def load_task_list(self): 
        try:
            with open(TASKFILE, 'r') as f:
                try: 
                    data = json.load(f, object_hook = json_deserializer)
                except ValueError: 
                    data = []
        except IOError:
            f = open(TASKFILE, 'w')
            f.close()
            data = []

        task_list = []
        for datum in data:
            t = Task(datum)
            task_list.append(t)
        return task_list

    def save_task_list(self): 
        try:
            with open(TASKFILE, 'w') as f: 
                json.dump([t.get_data() for t in self.task_list], f, indent = 4, default = json_serializer)
        except IOError: 
            raise

    def add(self, task): 
        self.task_list.append(task)
        self.save_task_list()

    def get_new_id(self): 
        try:
            return max([t.get('ID') for t in self.task_list]) + 1
        except ValueError:
            return 1

    def get_new_priority(self): 
        try: 
            return max([t.get('priority') for t in self.task_list]) + 1
        except ValueError:
            return 1
    def get_tasks(self, filt): 
        # TODO: filter tasks according to filt.
        return self.get_task_list()

    def get_task_list(self): 
        return self.task_list

    def deleteDB(self, task): 
        os.remove('tasktimer/tasklist.json')


class CustomEncoder(json.JSONEncoder): 
    def default(self, obj): 
        pass


def json_deserializer(dct): 
    import datetime
    if '__datetime__' in dct: 
        dct = datetime.datetime.strptime(dct['__datetime__'], '%Y-%m-%dT%H:%M:%S.%f')
        assert(isinstance(dct, datetime.datetime))
    return dct

def json_serializer(obj):
    import datetime
    # replaces all datetime objects with dict {'__datetime__': <string representing date>} 
    if isinstance(obj, datetime.datetime):
        datetime_dict = {'__datetime__':  obj.isoformat()}
        return datetime_dict
    raise TypeError


