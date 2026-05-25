class Storage:
    def __init__(self, ram):
        self.ram =ram
        self.size = ram.return_size()**2
        self.data = [0]*self.size
        self.location_index={}
        self.map_name_key = {}

    def __str__(self):
        return f"Storage: {self.data}"

    def __getitem__(self, item):
        if item< len(self.data):
            return self.data[item]
        else:
            print('Data out of bounds')

    def __setitem__(self, address, value):
        if address<len(self.data):
            self.data[address]=value
        else:
            print("Data out of bounds")

    def store(self, value_to_store, storage_address):
        if storage_address<len(self.data):
            self.data[storage_address]=value_to_store
            self.location_index[storage_address]=value_to_store
            self.map_name_key[value_to_store[0][2]]=storage_address

    def storage_len(self):
        return len(self.data)

    #TODO HARD add equivalent of PID for storage