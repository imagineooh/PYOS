class Storage:
    def __init__(self, ram):
        self.ram =ram
        self.size = ram.return_size()**2
        self.data = [0]*self.size

    def __str__(self):
        return f"Storage: {self.data}"

    def store(self, value_to_store, storage_address):
        if storage_address<len(self.data):
            self.data[storage_address]=value_to_store


