from context import Context
from storage import Storage
import logging

class Inode:
    def __init__(self, ram, storage):
        self.ram = ram
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.counter = 0
        self.filename_index={}
        self.storage = storage
        self.authorisation=False
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
        self.pointers={}
        self.pointers_backup=[]
        self.reserved_spots = []
        self.authorized_processes = ["setuptool"]

    def reserve_spaces(self):
        self.reserved_spots = [0]

    def append_reserved_spot(self, address:int):
        self.reserved_spots.append(address)

    def signin(self):
        self.authorisation=True
    def add_inode(self, address: int, type_file:str, filename: str):
        if address in self.reserved_spots and filename not in self.authorized_processes:
            raise ReservedPointingError(f"Pointed to reserved address {address}")
        if type_file=='file' and self.ram[address]==0:
            if self.ram.write(address, [[address, type_file, filename], []], self.authorisation) != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [[address, type_file, filename], []], self.authorisation)
                self.filename_index[filename] = address
        elif type_file=='folder' and self.ram[address]==0:
            if self.ram.write(address, [[address, type_file, filename], {}], self.authorisation)  != "Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//":
                self.ram.write(address, [[address, type_file, filename], {}], self.authorisation)
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

    def locate_free_disk(self):
        free_area=[]
        for i in range(self.storage.storage_len()):
            if self.storage[i]==0:
                free_area.append(i)
        return free_area

    def read_file(self, address):
        return self.ram[address]

    def migrate_storage_ram(self, ram_address, filename):
        address = self.storage.map_name_key[filename]
        self.ram[ram_address] = self.storage[address]
        edit_tuple=list(self.ram[ram_address][0])
        edit_tuple[0]=ram_address
        self.ram[ram_address]=[edit_tuple, self.ram[ram_address][1]]
        self.filename_index[filename]=ram_address
        self.storage[address]=0

    def give_filename_index(self):
        return self.filename_index.values()

    def update_PID(self):
        for i in range(self.ram.len_RAM()):
            if self.ram[i]!=0:
                if self.ram[i][0][0]!=i:
                    self.ram[i][0][0]=i
                    self.filename_index[self.ram[i][0][2]]=i

    def reestablish_pid(self):
        temp=[0]*self.ram.len_RAM()
        for i in range(self.ram.len_RAM()):
            if self.ram[i]!=0:
                if self.ram[i][0][0]!=i:
                    temp[self.ram[i][0][0]]=self.ram[i]
                else:
                    temp[self.ram[i][0][0]]=self.ram[i]
        for k in range(len(temp)):
            self.ram[k] = temp[k]

    def percent_used(self):
        counter=0
        for i in range(self.ram.len_RAM()):
            if self.ram[i]!=0:
                counter+=1
        percent_usage=(100*counter)/self.ram.len_RAM()
        print(f'Ram used at {percent_usage}% ({counter} slots used for {self.ram.len_RAM()} slots)')
        first_str='-'*round(percent_usage/5)
        second_str='.'*round((100-counter)/5)
        print(f"[{first_str}{second_str}]")

    # I know I know, not my best copy-paste work from the function right above this one, but it works ok...
    def percent_used_storage(self):
        counter=0
        for i in range(self.storage.storage_len()):
            if self.storage[i]!=0:
                counter+=1
        percent_usage=(100*counter)/self.storage.storage_len()
        print(f'Storage used at {percent_usage}% ({counter} slots used for {self.storage.storage_len()} slots)')
        first_str='-'*round(percent_usage/5)
        second_str='.'*round((100-counter)/5)
        print(f"[{first_str}{second_str}]")

    def point_to_mutiple(self, pointer:list):
        if self.pointers:
            self.pointers_backup.append(list(self.pointers.values()))
            self.pointers={}
        for i, val in enumerate(pointer):
            if int(val)<self.ram.len_RAM():
                self.pointers[f"@{i}"]=self.ram[int(val)]
        return self.pointers

    def file_exists(self, filename:str):
        if filename in self.filename_index.keys():
            return True
        return False

    def del_checker(self, filename):
        del self.filename_index[filename]

class ReservedPointingError(Exception):
    pass