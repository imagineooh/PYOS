class Inode:
    def __init__(self, ram):
        self.ram = ram
        self.counter = 0
        self.filename_index={}
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
    def add_inode(self, address: int, type_file:str, filename: str):
        if type_file=='file':
            if self.ram.write(address, [(self.counter, type_file, filename), None]) != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [(self.counter, type_file, filename), None])
        elif type_file=='folder':
            if self.ram.write(address, [(self.counter, type_file, filename), []])  != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [(self.counter, type_file, filename), []])
                self.filename_index[filename]=address
        self.counter+=1

