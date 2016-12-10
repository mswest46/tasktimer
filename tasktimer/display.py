class Display(): 
    def __init__(self): 
        pass

    def show(self, tasks): 
        print('TASK LIST')
        for task in sorted(tasks, key = lambda t: t.get('priority')):
            print(task.data)
