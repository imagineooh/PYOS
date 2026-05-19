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
        self.commands_dict={
            "mkdir" : self.directory_manager.add_empty_folder,
            "mkdirfull" : self.directory_manager.add_folder,
            "end" : self.end,
        }

    def end(self):
        return 1

    def do_mkdir(self, arg):
        """Add a basic populated folder with no first file name"""
        args=arg.split()
        foldername=str(args[0])
        folderdata=list(args[1].split(","))
        address=int(args[2])
        self.directory_manager.add_empty_folder(foldername, folderdata, address)


    def do_mkdirfull(self, arg):
        """Add a populated folder with given first file name"""
        args = arg.split()
        foldername = str(args[0])
        folderdata = list(args[1].split(","))
        address = int(args[2])
        firstfilename = str(args[3])
        self.directory_manager.add_folder(foldername, folderdata, address, firstfilename)


    def do_exit(self, arg):
        """exit the terminal"""
        print("Leaving the TameOS virtual kernel. See you soon!")
        return True

    def do_lsram(self, arg):
        """Print RAM data to terminal"""
        print(ram)

    def do_touchfull(self, arg):
        """Add a populated file to RAM
Syntax: touchfull file_name file_data address"""
        args = arg.split()
        file_name = str(args[0])
        file_data = list(args[1].split(","))
        address = int(args[2])
        self.directory_manager.add_file(file_name, file_data, address)

TameShell(ram, storage).cmdloop()

