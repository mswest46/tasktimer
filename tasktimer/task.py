import uuid 
class Task(): 
    """ most of the time we're calling Task when reading from file. So constructor should
    take a data object which is just a dictionary. Passing a straight dict could go wrong
    if we forget to pass in identifiers/ other mandatory data. So we'll need a validate
    method too. """
    def __init__(self, data): 
        self.data = data

    @classmethod
    def brand_new(cls, description):
        data = {"uuid": 1, "description": description}
        return cls(data)

    def set(self, datum_name, datum): 
        assert(not self.data[datum_name])
        self.data[datum_name] = datum
    def change(self, datum_name, datum):
        assert(self.data[datum_name])
        self.data[datum_name] = datum
    def get(self, datum_name, datum): 
        assert(self.data[datum_name])
        return self.data[datum_name]
    def get_data(self): 
        return self.data


