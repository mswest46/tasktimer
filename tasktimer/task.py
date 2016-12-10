import uuid 
from datetime import datetime

class Task(): 
    """ most of the time we're calling Task when reading from file. So constructor should
    take a data object which is just a dictionary. Passing a straight dict could go wrong
    if we forget to pass in identifiers/ other mandatory data. So we'll need a validate
    method too. """
    def __init__(self, data): 
        self.data = data

    @classmethod
    def brand_new(cls, **kwargs ):
        data = cls.fill_in_data(kwargs)
        return cls(data)

    @classmethod
    def fill_in_data(cls, data):
        if not 'creation_time' in data:
            data['creation_time'] = datetime.now()
        if not 'status' in data:
            data['status'] = 'pending' 
        if not 'estimate' in data:
            data['estimate'] = None
        return data

    def set(self, datum_name, datum): 
        assert(not self.data[datum_name])
        self.data[datum_name] = datum

    def change(self, datum_name, datum):
        self.data[datum_name] = datum

    def get(self, datum_name): 
        return self.data[datum_name]

    def get_data(self): 
        return self.data


