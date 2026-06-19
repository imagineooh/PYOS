from time import sleep

from manager import Manager
from ram import RAM
from directory import Directory
from storage import Storage
import inspect
from commands import help
from PCB import PCB
from context import Context
from inode import Inode, ReservedPointingError
from system import System, OverclockError
import sys
import logging


class TameShell():
    intro = "Welcome to TameOS! Type help <command> to get help on a command.\n"
    print(intro)

    def __init__(self,ram, storage):
        self.username = input('Username: ')
        self.password=input('Password: ')
        self.context_manager = Context()
        self.authenticated = True
        if not self.context_manager.login(self.username, self.password):
            print('Invalid credentials')
            self.authenticated = False
            return
        self.prompt = f"C://TameOS/user:{self.username}/terminal: "
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"User {self.username} has successfully logged in")
        self.storage = storage
        self.ram=ram
        self.inode=Inode(ram, storage)
        self.inode.reserve_spaces()
        self.directory_manager=Directory(ram, storage, self.inode)
        self.system_manager = System(55)
        self.process_manager = Manager(ram, self.directory_manager, self.system_manager, storage)
        self.system_manager.process_manager=self.process_manager
        self.pcb_manager = PCB(ram, self.directory_manager)
        self.process_manager.start_scheduling()
        if self.authenticated and self.context_manager.fetch_auth(self.username)==1:
            self.inode.signin()
        self.system_manager.run_diagnostic()
        self.directory_manager.check_for_duplicates()
        self.process_manager.aut_update_thread() #testing for safe production
        self.process_manager.garbage_collection_thread() #testing for safe production
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
            "dfdisk": self.directory_manager.percent_used_disk,
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
            "refpopstat":self.process_manager.populate_status,
            "popstat": self.process_manager.output_pop,
            "ptmany":self.directory_manager.pointermult,
            "ptexec":self.process_manager.exec_pointers
        }
        self.conversion_table={
            str:lambda x:str(x),
            int : lambda x: int(x),
            list : lambda x: [i if i.isdigit() else i for i in x.split(",")]
        }

    def end(self):
        print("Quitting TameOS. See you soon, and remember to Let It Happen!")
        sys.exit(0)


    def get_closest_command(self, command):
        CommandsSplit=list(self.commands_dict.keys())
        closest=[]
        for i in range(len(CommandsSplit)):
            if CommandsSplit[i][:2]==command[:2]:
                closest.append(list(self.commands_dict.keys())[i])
        return ", ".join(x for x in closest)
    def default(self,arg):
        args = arg.split()
        if not args:
            return
        keyword = str(args[0])
        if keyword not in list(self.commands_dict.keys()):
            print(f"Command not found. Did you mean {self.get_closest_command(keyword)}?")
        if keyword in self.commands_dict:
            func = self.commands_dict[keyword]
            sig=inspect.signature(func)
            params=list(sig.parameters.values())
            user_args=args[1:]
            if len(args)==1 and len(sig.parameters.values())>0:
                print(sig)

            if len(args)>1:
                call_args = []
                for i in range(len(user_args)): #note to self: sig.parameters.values() contains even optional parameters
                    param_name=list(sig.parameters.keys())[i]
                    type=sig.parameters[param_name].annotation
                    call_args.append(self.conversion_table[type](user_args[i]))
            else:
                call_args=[]
            try:
                sig = inspect.signature(func)
                bound = sig.bind_partial(*call_args)
                bound.apply_defaults()
                return func(*bound.args, **bound.kwargs)
            except (TypeError,
                    IndexError,
                    KeyError,
                    ValueError,
                    AttributeError,) as e: #FIX HERE FOR RUNTIME ERRORS
                self.logger.error(f"Inputed Arg Error {e} after input '{''.join(args)}'", exc_info=True)
                return None
            except OverclockError as e:
                self.logger.error(f"Cpu usage spiked and caused an overclock."
                      f"Current threads: {self.system_manager.running_threads}"
                      f"Current Cpu usage: {self.system_manager.cpu_usage}", exc_info=True)
                sleep(0.4)
                self.process_manager.aut_update_thread()
                self.system_manager.run_diagnostic()
                return None
            except ReservedPointingError as e:
                print(e)
                return None

    def loop(self):
        if not self.authenticated:
            return
        while True:
            try:
                arg = input(self.prompt)
                if self.default(arg)==-1:
                    break
            except EOFError:
                break



