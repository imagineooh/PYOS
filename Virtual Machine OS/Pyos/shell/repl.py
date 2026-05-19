from cmd import Cmd
from manager import Manager
from ram import RAM
from directory import Directory
from storage import Storage
import inspect

ram=RAM(16)
storage=Storage(ram)
class TameShell():
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
            "lsram": lambda:print(ram),
        }

    def end(self):
        print("Quitting TameOS. See you soon!")
        return True

    def default(self,arg):
        args = arg.split()
        keyword = str(args[0])
        if keyword in self.commands_dict:
            func = self.commands_dict[keyword]

            call_args = []
            if len(args) > 1:
                call_args.append(args[1])
            if len(args) > 2:
                call_args.append(args[2].split(","))
            if len(args) > 3:
                call_args.append(int(args[3]))


            try:
                sig = inspect.signature(func)
                bound = sig.bind_partial(*call_args)
                bound.apply_defaults()
                return func(*bound.args, **bound.kwargs)
            except TypeError as e:
                print(f"Arg error {e}")
                return None

    def loop(self):
        while True:
            try:
                arg = input(TameShell.prompt)
                if self.default(arg):
                    break
            except EOFError:
                break

shell = TameShell(ram, storage)
shell.loop()

