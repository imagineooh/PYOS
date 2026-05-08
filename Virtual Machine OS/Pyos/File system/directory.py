from inode import Inode

class Directory:
    def __init__(self,  ram):
        self.ram = ram
        self.inode_manager=Inode(ram)
        self.ram.sign_in('F', 'pas')
        self.ram.add_user('F', 'pas')

    class TreeNode:
        def __init__(self, number, name):
            self.number =  number
            self.name = name
            self.children = []
        def add_child(self, child):
            self.children.append(child)

    def add_empty_file(self, filename: str, address:int) -> None:
        self.ram.add_file(address, filename)

    def add_inode(self, address: int, type_file:str, filename: str):
        self.inode_manager.add_inode(address, type_file, filename)





