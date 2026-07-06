import time
from threading import Thread

from context import Context
from storage import Storage
import logging

class Inode:
    def __init__(self, ram, storage, system):
        self.ram = ram
        self.system_manager = system
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.ramlogger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        handler = logging.FileHandler("TameOSramlog.log", mode='w')
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.ramlogger.addHandler(handler)
        self.counter = 0
        self.filename_index={}
        self.storage = storage
        self.authorisation=False
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
        self.pointers={}
        self.pointers_backup=[]
        self.reserved_spots = []
        self.free_reserved_spots = []
        self.authorized_processes = ["setuptool"]
        self.auth_checking_status : bool = True

    def reserve_spaces(self):
        self.reserved_spots = list(range(0,3))

    def append_reserved_spot(self, address:int):
        self.reserved_spots.append(address)

    def add_authorized_process(self, processname:str):
        if processname in self.authorized_processes:
            pass
        else:
            self.authorized_processes.append(processname)

    def remove_free_spot(self, element: int) -> None: #void function
        #note: self.free_reserved_spots : list[int]
        try:
            if element not in self.free_reserved_spots:
                raise NonPresentAuthIDError("Non present authID in authorized processes")
            self.free_reserved_spots.remove(element)
        except ValueError:
            pass
        except NonPresentAuthIDError:
            self.ramlogger.info(f"Could not find element {element} in prerequisite auth ID elements")

    def add_free_spot(self, element:int):
        try:
            if element in self.free_reserved_spots:
                raise AlreadyPresentAuthIDError("Already present authID in authorized processes")
            self.free_reserved_spots.append(element)
        except AlreadyPresentAuthIDError:
            self.ramlogger.info(f"The element {element} which is a part of the prerequisite auth ID elements is already free")

    def update_free_spots_thread(self):
        local_thread_id = '0x008'
        def update_return_base():
            nonlocal local_thread_id
            while True:
                try:
                    if self.auth_checking_status:
                        for i in self.reserved_spots:
                            if self.ram[i] !=0:
                                self.remove_free_spot(i)
                            else:
                                self.add_free_spot(i)
                        self.ramlogger.info(f"Thread{local_thread_id} updated free auth processes")
                except RuntimeError:
                    self.logger.error(exc_info=True)
                    continue
                finally:
                    time.sleep(0.3)
        self.system_manager.create_thread_id(local_thread_id)
        t1 = Thread(target=update_return_base)
        t1.start()
    def get_smallest_reserved(self) -> int:
        """
        Getter function for getting the smallest possible
        reserved ram address for custom processes
        :return: Int, RAM address
        """
        try:
            self.auth_checking_status = False
            smallest_index=min(self.free_reserved_spots)
            self.auth_checking_status = True
            #self.logger.warning(f"smallest index found for auth processes is {smallest_index}")
            return smallest_index
        except ValueError:
            self.logger.warning("List free_reserved_spots is empty, resetting")
            self.init_auth()
            return min(self.free_reserved_spots)

    def init_auth(self):
        self.free_reserved_spots = list(self.reserved_spots)

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

class NonPresentAuthIDError(Exception):
    pass

class AlreadyPresentAuthIDError(Exception):
    pass
