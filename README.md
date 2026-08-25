# TameOS, the fully python virtual operating system


This is, above all, a learning experience. I do not, and did not expect to make a fully optimised virtual OS software. The code is mainly a proof of concept/stepping stone, and is based on real systems and subsystems. The OS is fully written and designed by hand after thorough research through pretty much any resource and technology I could find and harness to learn, which also helped me discover new optimisation techniques. 
And, don’t forget, the project is just getting started.

## Functionalities
- Full Host OS (windows for now) TameOS communication
- FIFO scheduler based on file longevity
- Directory and FileSystem (working on Inode)
- Context and autonomous REPL, with commands help function
- ProcessControlBlock to track active and inactive slots (used for scheduling)
- System Manger to throttle activities and manage threads
- Logger system
- Compiler for TameOS custom machine language (not yet finished)
- Process Manager working on precise data packaging to decrypt and encrypt data (works on Cpython concepts), here is an interesting exerpt (only a small part of the file, ignore GC and most other functions):
  - The aut_update_file function:
    ```py
    def auto_update_file(self, runtime_arg:str):
        self.migrator_counter+=1
        #mig_name=f"0x001.{self.migrator_counter}"
        while self.system_monitor.thread_id[runtime_arg]!=0:
            runnin_process_copy = list(self.running_processes.items())
            for foldername, values in runnin_process_copy:
                sleep(1)
                filename = values[0]
                address=values[1]
                migratorname:str = f"setuptool{self.migrator_counter}"
                self.directory_manager.add_auth_process(migratorname)
                setup_address = self.directory_manager.smauthID()
                try:
                    storage_address = self.directory_manager.get_storage_address(foldername)
                    self.migrate_host_ram(filename, ".txt", migratorname, setup_address)
                    data=self.ram[0][1][filename][:2]
                    self.storage[storage_address][1][filename]=[data, 0]
                except RuntimeError as e:
                    self.logger.error("Runtime error in thread", exc_info=True)
                except KeyError as e:
                    self.logger.warning("Keyerror occured", exc_info=True)
                except:
                    continue
                finally:
                    if self.directory_manager.file_exists(migratorname):
                        self.directory_manager.delete_slots(setup_address)
        self.logger.info(f"Thread {runtime_arg} closed fully")
    ```
    This function (which runs in a thread) activelly migrates the create file with ptexec (which adds the value to running_processes), and is considered the most CPU taking function, so it is the first to stop in case of the custom OverclockError.
    
There are many more interesting function, which I will not mention here, as they would pollute the README, including the custom garbage collector and others.
For a full list of all commands, simply type help after running main.py.

## How it works:
TameOS functions on a working, fully custom-made shell (shell->repl.py, made with custom function inspection for faster metadata analysis and dispatch), custom made file system and directory, built on an Inode manager. The inode’s main job is to format the files in ram, so that the process manager (which runs files) maps exactly to the data it needs. 
The process manager is the central piece of the computing unit: it dispatches the different multi pointers to threads, which run .txt, .wav and most importantly .exe files from the host OS. Once the files are migrated, TameOS takes full responsibility of file security and memory management for those files directly in TameOS (any modifications you make to the file will affect the file even in your host OS environment, looking into making the file completely local to TameoS at the moment, not guarenteed to protect if host OS does anything), as they do not require the user to fetch directly from the OS (TameOS does that on a separate thread automatically). There is a custom pager for inter-memory communication that was put in place, and handles migration between disk (non volatile memory) and RAM (volatile memory), and some portions of RAM are allocated to internal systems that ensure the proper functioning of the processing and filing. The Garbage Collector depends on the slot being explicitly market as _inactive_ for the gc to pick it up. GC works on a timestamp based marking by the scheduler, marking files as inactive after 5 seconds of being idle in RAM. This drastically frees RAM, and has been seen to help for excessive allocation of variables. 

For thread and CPU security, a custom made system monitor (with thread ID tracker) tracks cpu usage vs expected max usage, and has custom made exceptions to halt processes and save CPU performance. 

To check out the system logs, there are three main .log files: TameOSlog for general logs and some memory, TameOSramlog for anything memory related and finally TameOSschedlog for timestamp verification.

## Struggles:
The main struggles were getting the opening of executable files and and saving to local TameOS memory, as you will be able to see in the commit log history. 
Dependency injection was also a struggle, as inter-communicating three separate systems with internal subsystems was a mess, and the use of OOP for this very struggle was mandatory.

## GIT history:
I recommend taking a look into the commit history for this project, as well as comments, as you can see my journey in learning this project.

## In the making

I am currently working on a custom compiler working on the Virtual OS, check it out in shell->compiler. As of today, the program can do correct operations, and the basic `jump` operation.

## Final note:

This project took A LOT of my time, and I hope you will find it as exciting as me to discover the magical world of Virtual Operating System sandboxes. I am always free to contact on the issue or discussion if you want to contribute to this adventure, or simply as a question! 

Thank you,

Imagineooh

