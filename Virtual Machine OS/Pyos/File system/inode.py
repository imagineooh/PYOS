from storage import Storage

class Inode:
    def __init__(self, ram, storage):
        self.ram = ram
        self.counter = 0
        self.filename_index={}
        self.storage = storage
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
    def add_inode(self, address: int, type_file:str, filename: str):
        if type_file=='file' and self.ram[address]==0:
            if self.ram.write(address, [(self.counter, type_file, filename), None], True) != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [(self.counter, type_file, filename), None], True)
                self.filename_index[filename] = address
        elif type_file=='folder' and self.ram[address]==0:
            if self.ram.write(address, [(self.counter, type_file, filename), {}], True)  != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [(self.counter, type_file, filename), {}], True)
                self.filename_index[filename]=address




        self.counter+=1
    def locate_object(self, name: str):
        return self.filename_index[name]

    def return_all_used_slots(self):
        return list(self.filename_index.values())

    def edit_file(self, address:int, new_data: list, new_data_name: str):
        self.ram[address][1][new_data_name] = new_data

    def delete_data(self, address):
        self.ram[address][1]=0

    def delete_slots(self, address):
        self.ram[address]=0
        for key, value in list(self.filename_index.items()):
            if value == address:
                del self.filename_index[key]


    def store_value(self, value_to_store, storage_address): #equivalent of migrate_ram_process
        self.storage.store(value_to_store, storage_address)

    def read_file(self, address):
        return self.ram[address]

    def migrate_storage_ram(self, ram_address, filename):
        address = self.storage.map_name_key[filename]
        self.ram[ram_address]= self.storage[address]
        edit_tuple=list(self.ram[ram_address][0])
        edit_tuple[0]=ram_address
        self.ram[address]=[tuple(edit_tuple), self.ram[ram_address][1]]
        self.filename_index[filename]=ram_address

    def give_filename_index(self):
        return self.filename_index.values()


