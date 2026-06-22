# TameOS, the fully python virtual operating system


This is, above all, a learning experience. I do not, and did not expect to make a fully optimised virtual OS software. The code is mainly a proof of concept, and is based on real systems and subsystems. The OS is fully written and designed by hand after thorough research through pretty much any resource and technology I could find and harness to learn, which also helped me discover new optimisation techniques. 
And, don’t forget, the project is just getting started.

## Functionalities
- Full Host OS (windows for now) TameOS communication, fully safe
- FIFO scheduler (working to refactor on CPU-based scheduling)
- Directory and FileSystem (working on Inode)
- Context and REPL, with commands help function
- ProcessControlBlock to track active and inactive slots (used for scheduling)
- Process Manager working on precise data packaging to decrypt and encrypt data (works on Cpython concepts), here are a few interesting exerpts:
  - From the exec_wav function
    ```py
    def exec_wav(self, file_name, process_name):
        next_process_to_run = self.directory_manager.locate_object(process_name)
        packaging_info = list(self.ram[next_process_to_run][1][file_name][0])
        sample_rate = int.from_bytes(packaging_info[24:28], byteorder='little')
        audio_data = bytearray(self.ram[next_process_to_run][1][file_name][1])
        p = pyaudio.PyAudio()
    ```
    In this case, the packaging info is the informatio of the audio sequence that the user migrated from the host OS, but not the data itself. The data has to be a bytearray, as stream.write can only handle bytelike objects.
  - from the exec_pointers function:
    ```py
    elif extension==str(bin(2))[2:]:
                        if not subfile_name:
                            self.system_monitor.create_thread_id("0x004")
                            self.logger.info(f"Started thread 0x004 for decrypting exe files without subfile name")
                            t1 = threading.Thread(target=self.exec_exe,
                                                  args=(list(self.ram[index_ram][1].values())[DictLen][-4], index_ram))
                            t1.start()
                        else:
                            self.system_monitor.create_thread_id("0x005")
                            self.logger.info(f"Started thread 0x005 for decrypting exe files with subfile name")
                            self.running_processes[ProcessName]=[subfile_name, index_ram]
                            t1_pause_event = threading.Event()
                            t1_pause_event.set()
                            tfetcher_pause_event = threading.Event()
                            tfetcher_pause_event.set()
                            def fetcher(subfile_name, index_ram, pause_event):
                                pause_event.wait()
                                self.migrate_host_ram(subfile_name, '.txt', 'opened_file', index_ram)
                            t1 = threading.Thread(target=self.exec_exe,
                                                  args=(list(self.ram[index_ram][1].values())[DictLen][-4], index_ram, t1_pause_event, subfile_name))
                            tfetcher = threading.Thread(target=fetcher, args=(subfile_name, index_ram, tfetcher_pause_event))
                            t1.start()
                            tfetcher.start()
                            self.logger.info(f"Started thread tfecther (default) for decrypting exe files with subfile name")
    ```
    This function runs executable files in threads to make the operation non-blocking for the main thread, with fetcher only running once to start the active migration (which is actively followed by the auto_update_file func(see below).
  - The aut_update_file function:
    ```py
    ef auto_update_file(self, runtime_arg:str):
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
                    """metadata = list(self.storage[address][1].values())
                    processname = metadata[0]
                    print(f"Process name is {processname}")"""
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
    

For a full list of all commands, simply type help after running either repl.py or main.py (repl safer for now, testing is based there)

## How it works:
TameOS functions on a working, fully custom-made shell (shell->repl.py, made with custom function inspection for faster metadata analysis and dispatch), custom made file system and directory, built on an Inode manager. The inode’s main job is to format the files in ram, so that the process manager (which runs files) maps exactly to the data it needs. 
The process manager is the central piece of the computing unit: it dispatches the different multi pointers to threads, which run .txt, .wav and most importantly .exe files from the host OS. Once the files are migrated, TameOS takes full responsibility of file security and memory management for those files, as they do not require the user to fetch directly from the OS (TameOS does that on a separate thread automatically). There is a custom pager for inter-memory communication that was put in place, and handles migration between disk (non volatile memory) and RAM (volatile memory), and some portions of RAM are allocated to internal systems that ensure the proper functioning of the processing and filing. 
For thread and CPU security, a custom made system monitor (with thread ID tracker) tracks cpu usage vs expected max usage, and has custom made exceptions to halt processes and save CPU performance. 

## Struggles:
The main struggles were getting the opening of executable files and and saving to local TameOS memory, as you will be able to see in the commit log history. 
Dependency injection was also a struggle, as inter-communicating three separate systems with internal subsystems was a mess, and the use of OOP for this very struggle was mandatory.

## GIT history:
I recommend taking a look into the commit history for this project, as well as comments, as you can see my journey in learning this project.


## Final note:

This project took A LOT of my time, and I hope you will find it as exciting as me to discover the magical world of Virtual Operating System sandboxes. I am always free to contact on the issue or discussion if you want to contribute to this adventure, or simply as a question! 

Thank you,
Imagineooh

