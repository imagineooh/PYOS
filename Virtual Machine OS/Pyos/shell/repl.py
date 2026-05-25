from manager import Manager
from ram import RAM
from directory import Directory
from storage import Storage
import inspect
from commands import help
from PCB import PCB

ram=RAM(16)
storage=Storage(ram)
class TameShell():
    username = 'flav'
    intro = "Welcome to TameOS! Type help <command> to get help on a command.\n"
    print(intro)
    prompt = f"C://TameOS/user:{username}/terminal: "

    def __init__(self,ram, storage):
        self.storage = storage
        self.ram=ram
        self.directory_manager=Directory(ram, storage)
        self.process_manager = Manager(ram, self.directory_manager)
        self.pcb_manager = PCB(ram, self.directory_manager)
        self.commands_dict={
            "mkdir" : self.directory_manager.add_empty_folder,
            "mkfolder" : self.directory_manager.add_folder,
            "end" : self.end,
            "lsram": lambda:print(ram),
            "help": help,
            "mod":self.directory_manager.edit_file,
            "write": self.directory_manager.store_value,
            "ramstage":self.directory_manager.migrate_storage_ram,
            "df":self.directory_manager.percent_used,
            "pidasync":self.directory_manager.update_PID,
            "idlescan":self.pcb_manager.track_inactivity,
            "purge":self.process_manager.delete_inactive_slots,
            "next":self.process_manager.process_to_run,
            "sched":self.process_manager.schedule_process_all,
            "exec":self.process_manager.run_slots,
            "malloc":self.process_manager.allocate_area,
            "lsdisk":lambda:print(storage),
            "deldata":self.directory_manager.delete_folder_data,
            "hostex":self.process_manager.execute_path,
            "hostmig":self.process_manager.migrate_host_ram,
            "comem":self.process_manager.auto_migration_status,
        }
        self.conversion_table={
            str:lambda x:str(x),
            int : lambda x: int(x),
            list : lambda x: [i if i.isdigit() else i for i in x.split(",")]
        }
    def end(self):
        print("Quitting TameOS. See you soon!")
        return True

    def default(self,arg):
        args = arg.split()
        keyword = str(args[0])
        if keyword in self.commands_dict:
            func = self.commands_dict[keyword]
            sig=inspect.signature(func)
            params=list(sig.parameters.values())
            user_args=args[1:]
            if len(args)==1 and len(sig.parameters.values())>0:
                print(str(inspect.signature(func).parameters))

            if len(args)>1:
                call_args = []
                for i in range(len(user_args)): #note to self: sig.parameters.values() contains even optional parameters
                    param_name=list(inspect.signature(func).parameters.keys())[i]
                    type=inspect.signature(func).parameters[param_name].annotation
                    call_args.append(self.conversion_table[type](user_args[i]))
            else:
                call_args=[]
            try:
                sig = inspect.signature(func)
                bound = sig.bind_partial(*call_args)
                bound.apply_defaults()
                return func(*bound.args, **bound.kwargs)
            except (TypeError, IndexError, KeyError, ValueError) as e: #FIX HERE FOR RUNTIME ERRORS
                print(f"Inputed Arg Error {e} after input '{''.join(args)}'")
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

