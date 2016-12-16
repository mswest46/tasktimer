import uuid 
from datetime import datetime

STATUS_KEY = 'status'
ID_KEY = 'ID'
DESCRIPTION_KEY = 'description'
START_TIME_KEY = 'start_time'
END_TIME_KEY = 'end_time'


PENDING = 'pending'
COMPLETE = 'complete'
IN_PROGRESS = 'progress'
PAUSED = 'paused'


class Task(): 
    """ most of the time we're calling Task when reading from file. So constructor should
    take a data object which is just a dictionary. Passing a straight dict could go wrong
    if we forget to pass in identifiers/ other mandatory data. So we'll need a validate
    method too. """
    def __init__(self, data): 
        self.validate(data) 
        self.data = data
    
    def start(self): 
        self.set(STATUS_KEY, IN_PROGRESS)
        self.set(START_TIME_KEY, datetime.now())

    def finish(self): 
        self.set(STATUS_KEY,  COMPLETE)
        self.set(END_TIME_KEY, datetime.now())

    def pause(self): 
        # TODO: this messes up time
        self.set(STATUS_KEY, PAUSED)

    def has(self, datum_name): 
        return datum_name in self.data

    def set(self, datum_name, datum): 
        self.data[datum_name] = datum

    def get(self, datum_name): 
        return self.data[datum_name]
    
    def get_progress(self): 
        if self.get('status') == IN_PROGRESS:
            return datetime.now() - self.get(START_TIME_KEY)
        elif self.get('status') == COMPLETE:
            return self.get(END_TIME_KEY) - self.get(START_TIME_KEY)
        else:
            return None



    def get_data(self): 
        return self.data
    
    def validate(self, data): 
        assert (data['ID'] and 
                data['description'] and 
                data['status'] and 
                data['created']) 

