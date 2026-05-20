from inode import Inode
from filesystem import FileSystem

class Directory:
    def __init__(self,  ram, storage):
        self.ram = ram
        self.inode_manager=Inode(ram, storage)
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
        self.file_manager=FileSystem(ram, storage)

    class Folder:
        def __init__(self, number, name):
            self.number =  number
            self.name = name
            self.children = []
        def add_child(self, child):
            self.children.append(child)

    def add_empty_folder(self, foldername: str, folderdata: list,  address:int) -> None:
        self.file_manager.construct_empty_folder(foldername, folderdata, address)
        self.update_PID()

    def add_file(self, file_name, file_data, address):
        self.file_manager.construct_single_file(file_name,file_data, address)

    def add_folder(self, foldername: str, folderdata: list, address: int, firstfilename: str) -> None:
        self.file_manager.construct_folder(foldername,folderdata, address, firstfilename)
        self.update_PID()

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
        self.file_manager.delete_slots(address)
        self.update_PID()

    def store_value(self, foldername: str, storage_address: int):
        ram_address=self.file_manager.locate_object(foldername)
        to_store=self.file_manager.read_file(ram_address)
        self.file_manager.store_value(to_store, storage_address)

    def migrate_storage_ram(self, address: int, filename:str):
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
