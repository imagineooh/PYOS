from inode import Inode
from filesystem import FileSystem
from directory import Directory

class PCB:
    def __init__(self, ram):
        self.ram = ram
        self.inode_manager = Inode(ram)
        self.file_manager = FileSystem(ram)
        self.directory_manager = Directory(ram)
        self.used_slots=[]
        self.inactive_slots=[]

    def track_used(self) -> None:
        self.used_slots=[]
        for key in self.directory_manager.return_all_used_slots():
            self.used_slots.append(key)

    def update_inactivity(self):
        for address in enumerate(self.directory_manager.return_all_used_slots()):
            if self.ram[address][1] == 0:
                self.inactive_slots.append(address)
                print(self.inactive_slots)
        if len(self.inactive_slots)==0:
           print('All slots are active')
           print(self.inactive_slots)

