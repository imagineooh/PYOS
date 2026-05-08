from inode import Inode
from filesystem import FileSystem

class Directory:
    def __init__(self,  ram):
        self.ram = ram
        self.inode_manager=Inode(ram)
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')
        self.file_manager=FileSystem(ram)

    class TreeNode:
        def __init__(self, number, name):
            self.number =  number
            self.name = name
            self.children = []
        def add_child(self, child):
            self.children.append(child)

    def add_empty_folder(self, foldername: str, folderdata: list,  address:int) -> None:
        self.file_manager.construct_folder(foldername, folderdata, address)

    def add_file(self, file_name, file_data, address):
        self.file_manager.construct_file(file_name,file_data, address)


    def add_inode(self, address: int, type_file:str, filename: str):
        self.inode_manager.add_inode(address, type_file, filename)





