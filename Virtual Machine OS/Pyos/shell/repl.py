from cmd import Cmd
from manager import Manager
from ram import RAM
from directory import Directory
from storage import Storage

ram=RAM(16)
storage=Storage(ram)
class TameShell(Cmd):
    username = 'flav'
    intro = "Welcome to TameOS! Type help or ? to list commands.\n"
    prompt = f"C://TameOS/user:{username}/terminal: "

    def __init__(self,ram, storage):
        super().__init__()
        self.storage = storage
        self.ram=ram
        self.directory_manager=Directory(ram, storage)
        self.process_manager = Manager(ram, storage)

    def do_mkdir(self, arg):
        args=arg.split()
        foldername=str(args[0])
        folderdata=list(args[1].split(","))
        address=int(args[2])
        self.directory_manager.add_empty_folder(foldername, folderdata, address)
        print(ram)

    def do_mkdirfull(self, arg):
        args = arg.split()
        foldername = str(args[0])
        folderdata = list(args[1].split(","))
        address = int(args[2])
        firstfilename = str(args[3])
        self.directory_manager.add_folder(foldername, folderdata, address, firstfilename)
        print(ram)

    def do_exit(self, arg):
        print("Leaving the TameOS virtual kernel. See you soon!")
        return True
TameShell(ram, storage).cmdloop()

