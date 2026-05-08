from inode import Inode

class FileSystem:
    def __init__(self, ram):
        self.ram = ram
        self.inode_manager =Inode(ram)
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')

    def construct_folder(self, folder_name: str, folder_data: list, address:int):
        if self.ram[address] == 0:
            self.inode_manager.add_inode(address, 'folder', folder_name)
            self.ram[address][1].append(folder_data)

    def construct_file(self, file_name: str, file_data: list, address:int):
        if self.ram[address]==0:
            self.inode_manager.add_inode(address, 'file', file_name)
            self.ram[address][1].append(file_data)
