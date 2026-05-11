from inode import Inode

class FileSystem:
    def __init__(self, ram, storage):
        self.ram = ram
        self.inode_manager =Inode(ram, storage)
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')

    def construct_single_file(self, file_name: str, file_data: list, address:int):
        if self.ram[address]==0:
            self.inode_manager.add_inode(address, 'file', file_name)
            self.ram[address][1].append(file_data)


    def construct_empty_folder(self, folder_name: str, folder_data: list, address:int):
        if self.ram[address] == 0:
            self.inode_manager.add_inode(address, 'folder', folder_name)
            self.ram[address][1]["first_commit"]=folder_data

    def construct_folder(self, folder_name: str, folder_data: list, address:int, first_file_name: str):
        if self.ram[address] == 0:
            self.inode_manager.add_inode(address, 'folder', folder_name)
            self.ram[address][1][first_file_name]=folder_data

    def locate_object(self, name):
        return self.inode_manager.locate_object(name)

    def edit_file(self, address: int, new_data: list, new_data_name: str):
        self.inode_manager.edit_file(address,new_data,new_data_name)

    def delete_data(self, address):
        self.inode_manager.delete_data(address)

    def return_all_used_slots(self):
        return self.inode_manager.return_all_used_slots()

    def delete_slots(self, address):
        self.inode_manager.delete_slots(address)

    def store_value(self, value_to_store, storage_address):
        self.inode_manager.store_value(value_to_store, storage_address)

    def read_file(self, address):
        return self.inode_manager.read_file(address)

    def migrate_storage_ram(self, address, filename):
        self.inode_manager.migrate_storage_ram(address, filename)
