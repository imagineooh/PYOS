class Inode:
    def __init__(self, ram):
        self.ram = ram
        self.counter = 0
        self.filename_index={}
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
        slots=[]
        for i in self.filename_index.keys():
            slots.append(i)
        return slots



    def edit_file(self, address:int, new_data: list, new_data_name: str):
        self.ram[address][1][new_data_name] = new_data

    def delete_data(self, address):
        self.ram[address][1]=0

