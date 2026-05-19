from manager import Manager
from ram import RAM
from directory import Directory
from storage import Storage

class Commands(dict):
    def __init__(self,ram, storage):
        self.storage = storage
        self.ram=ram
        self.directory_manager=Directory(ram, storage)
        self.process_manager = Manager(ram, storage)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        print('GET', key)
        return val

    def __setitem__(self, key, val):
        print('SET', key, val)
        dict.__setitem__(self, key, val)



