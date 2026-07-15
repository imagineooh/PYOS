from inode import Inode
from filesystem import FileSystem
from threading import Thread
from time import sleep

class Directory:
    def __init__(self,  ram, storage, inode):
        self.ram = ram
        self.inode_manager=inode
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
        self.file_manager=FileSystem(ram, storage, self.inode_manager)
        self.pointers=[]
        self.duplicates=[] #returns PID of duplicates in RAM
        self.storage_pointers = {}
        self.base_var_spots = [i for i in range(10,110)]
        self.var_heap = [i for i in range(110, 150)]
        self.free_var_spots=list(self.base_var_spots)


    class Folder:
        def __init__(self, number, name):
            self.number =  number
            self.name = name
            self.children = []
        def add_child(self, child):
            self.children.append(child)

    def add_empty_folder(self, foldername: str, folderdata: list,  address:int) -> None:
        if self.inode_manager.file_exists(foldername):
            print("File already exists in directory")
            return
        self.file_manager.construct_empty_folder(foldername, folderdata, address)
        self.update_PID()

    def add_file(self, file_name, file_data, address):
        self.file_manager.construct_single_file(file_name,file_data, address)

    def add_folder(self, foldername: str, folderdata: list, address: int, firstfilename: str) -> None:
        if self.inode_manager.file_exists(foldername):
            print(f"File {foldername} already exists in directory")
            return
        self.file_manager.construct_folder(foldername,folderdata, address, firstfilename)
        self.update_PID()

    def add_variable(self, var_name:str, var_value:str, address:int, var_type:str | None = None):
        if self.inode_manager.file_exists(var_name) and var_type=="const":
            print(f"File {var_name} already exists in directory, spawned in DIR")
            return
        self.file_manager.construct_variable(var_name, var_value, address)
        self.update_PID()

    def vfree_spot(self, local:bool = False)->int:
        """
        Returns index for commiting the
        :param local: Bool, False if global, True if local
        :return: index
        """
        if not local:
            found_address = self.free_var_spots.pop(self.free_var_spots.index(min(self.free_var_spots)))
            return found_address
        return self.var_heap.pop(self.var_heap.index(min(self.var_heap)))

    def add_inode(self, address: int, type_file:str, filename: str):
        self.inode_manager.add_inode(address, type_file, filename)

    def edit_file(self, filename: str, data: list, new_data_name:str):
        address = self.file_manager.locate_object(filename)
        self.file_manager.edit_file(address, data, new_data_name)

    def locate_object(self, filename) ->int:
        return self.file_manager.locate_object(filename)

    def delete_folder_data(self, foldername:str):
        address=self.file_manager.locate_object(foldername)
        self.file_manager.delete_data(address)
        self.update_PID()

    def return_all_used_slots(self):
        return self.file_manager.return_all_used_slots()

    def delete_slots(self, address):
        #foldername = self.ram[address][0][2]
        #print(f'deleting {foldername}')
        self.file_manager.delete_slots(address)
        #self.inode_manager.del_checker(foldername)
        self.update_PID()

    def store_value(self, foldername: str, storage_address: int):
        ram_address=self.file_manager.locate_object(foldername)
        to_store=self.file_manager.read_file(ram_address)
        self.file_manager.store_value(to_store, storage_address)
        self.storage_pointers[foldername]=storage_address

    def get_storage_address(self, foldername:str):
        return self.storage_pointers[foldername]

    def free_disk_space(self): #TODO review possible 3ring failure here
        free_space=self.inode_manager.locate_free_disk()
        return free_space

    def migrate_storage_ram(self, filename:str, address: int):
        self.file_manager.migrate_storage_ram(address, filename)
        self.update_PID()

    def give_filename_index(self):
        return self.file_manager.give_filename_index()

    def update_PID(self):
        self.inode_manager.update_PID()

    def reestablish_PID(self): #very slow
        print("This method is slow, and could be unsafe")
        self.inode_manager.reestablish_pid()

    def percent_used(self):
        self.inode_manager.percent_used()

    def percent_used_disk(self):
        self.inode_manager.percent_used_storage()

    def is_in(self):
        self.inode_manager.signin()

    def pointermult(self, pointer:list):
        pointers=self.inode_manager.point_to_mutiple(pointer)
        print(pointers)
        self.pointers=pointers
        return pointers

    def check_for_duplicates_thread(self):
        """
        Is a threading.Thread type used for looking for duplicate files in RAM
        Searches with object_name, not file data (would take too long)
        :return: None (duplicates lives in shared duplicates array
        """
        while True:
            self.duplicates=[]
            checked=[]
            for i in range(self.ram.len_RAM()):
                if self.ram[i]!=0:
                    object_name=self.ram[i][0][2]
                    if object_name in checked:
                        self.duplicates.append(self.ram[i][0][0])
                        #print(f"found duplicate with PID: {self.ram[i][0][0]} in RAM")
                        self.delete_slots(i)
                    else:
                        checked.append(object_name)
            sleep(2)

    def check_for_duplicates(self):
        duplicate_thread=Thread(target=self.check_for_duplicates_thread)
        duplicate_thread.start()

    def replace_data(self, processname:str, address:int, new_data: any):
        if self.ram[address]!=0:
            self.ram[address][1][processname]=new_data

    def file_exists(self, filename:str):
        return self.inode_manager.file_exists(filename)

    def add_auth_process(self, pname:str):
        self.inode_manager.add_authorized_process(pname)

    def smauthID(self):
        return self.inode_manager.get_smallest_reserved()