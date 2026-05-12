from inode import Inode
from filesystem import FileSystem
from directory import Directory

class PCB:
    def __init__(self, ram, directory_manager):
        self.ram = ram
        self.directory_manager = directory_manager
        self.used_slots=[]
        self.inactive_slots=[]

    def track_used(self):
        self.used_slots=[]
        for key in self.directory_manager.return_all_used_slots():
            self.used_slots.append(key)
        return self.used_slots

    def update_inactivity(self):
        for address in self.directory_manager.return_all_used_slots():
            if self.ram[address][1] == 0:
                self.inactive_slots.append(address)

    def track_inactivity(self):
        self.update_inactivity()
        if len(self.inactive_slots)==0:
            print("All slots active")
        else:
            print(f'slots number {", ".join(str(x) for x in self.inactive_slots)} are inactive')

    def delete_inactive_slots(self):
        self.update_inactivity()
        for i in range(len(self.inactive_slots)):
            self.directory_manager.delete_slots(self.inactive_slots[i])

