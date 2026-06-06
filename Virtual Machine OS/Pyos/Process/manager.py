from scheduler import Scheduler
from PCB import PCB
from pathlib import Path
import pyaudio
import keyboard
import threading

class Manager:
    def __init__(self, ram, directory_manager):
        self.ram = ram
        self.start_signal = False
        self.directory_manager = directory_manager
        self.scheduler_manager = Scheduler(ram, directory_manager)
        self.pcb_manager = PCB(ram, directory_manager)
        self.auto_migrate=True

    def start_scheduling(self):
        self.start_signal=True

    def auto_migration_status(self, status:str):
        if status=='enable':
            self.auto_migrate=True
        elif status=='disable':
            self.auto_migrate=False
        else:
            print("Unknown command for auto_migrate")

    def track_inactivity(self):
        self.pcb_manager.track_inactivity()
        print(self.pcb_manager.track_inactivity())

    def update_inactivity(self):
        self.pcb_manager.update_inactivity()
        print(self.pcb_manager.update_inactivity())

    def track_used(self):
        self.pcb_manager.track_used()
        print(self.pcb_manager.track_used())

    def delete_inactive_slots(self):
        self.pcb_manager.delete_inactive_slots()

    def schedule_process_all(self):
        print(self.scheduler_manager.schedule_process_all())
        return self.scheduler_manager.schedule_process_all()

    def process_to_run(self):
        print(self.scheduler_manager.process_to_run())
        return self.scheduler_manager.process_to_run()

    def execute_path(self, path:str, extension:str):
        file_path = Path(f"C:/Users/pasca/Downloads/{path}{extension}")
        print(file_path)
        if file_path.exists():
            with open(file_path, 'r') as file:
                content=file.read()
                print(content)
        else:
            print("Could not find path in host OS")
    def exec_txt(self, file_name, process_name):
        next_process_to_run = self.directory_manager.locate_object(process_name)
        decrypt = []
        data = list(self.ram[next_process_to_run][1][file_name][0])
        for i in range(len(data)):
            decrypt.append(chr(int(data[i], 2)))
        self.scheduler_manager.mark_as_active(next_process_to_run)
        print("".join(x for x in decrypt))
        self.scheduler_manager.mark_as_inactive(next_process_to_run)

    def exec_wav(self, file_name, process_name):
        next_process_to_run = self.directory_manager.locate_object(process_name)
        packaging_info = list(self.ram[next_process_to_run][1][file_name][0])
        sample_rate = int.from_bytes(packaging_info[24:28], byteorder='little')
        audio_data = bytearray(self.ram[next_process_to_run][1][file_name][1])
        p = pyaudio.PyAudio()
        if int.from_bytes(packaging_info[34:36],
                          byteorder='little') == 16:  # from bytes defaults to big_endian, so we have to specify byteorder as 'little' for it to work
            format = pyaudio.paInt16
        else:
            format = pyaudio.paInt8
        channels = int.from_bytes(packaging_info[22:24], byteorder='little')
        rate = sample_rate
        stream = p.open(
            format=format,
            channels=channels,
            rate=rate,
            output=True,
            frames_per_buffer=1024,
        )
        done = False
        chunk = 0
        chunk_offset = 4096
        self.scheduler_manager.mark_as_active(next_process_to_run)
        while not done and chunk < len(audio_data):
            if chunk + chunk_offset < len(audio_data):
                stream.write(bytes(audio_data[chunk:(chunk + chunk_offset)]))
            else:
                stream.write(bytes(audio_data[chunk:]))
            if keyboard.is_pressed('q'):  # audio should stop playing
                self.scheduler_manager.mark_as_inactive(next_process_to_run)
                done = True
            chunk += chunk_offset

    def exec_exe(self, file_path, address:int, subfile_name:str=False):
        import subprocess  # TODO look into PATH
        self.scheduler_manager.mark_as_active(address)
        if subfile_name:
            subprocess.Popen([file_path, subfile_name], shell=False)
        else:
            subprocess.Popen(file_path, shell=False)

    def migrate_host_ram(self, path:str, extension:str, filename:str, address:int, file_location:str = None):
        #file_path = next(Path("C:\\").rglob(f"{filename}{extension}"), None) #As of now this does not work yet... Too slow
        if file_location is None:
            file_path = Path(f"C:/Users/pasca/Downloads/{path}{extension}")
        elif file_location=="stand":
            file_path=Path(f"C://Windows/{path}{extension}")
        else:
            file_path = Path(f"C:/Users/pasca/{file_location}/{path}{extension}")
        if file_path.exists():
            if extension=='.txt':
                with open(file_path, 'r') as file:
                    content = list(file.read())
                    content=[bin(ord(x))[2:] for x in content]
                self.directory_manager.add_folder(filename, [content, str(bin(0)[2:])], address, path)
            elif extension=='.wav':
                with open(file_path, 'rb') as file:
                    content = bytearray(file.read())
                    #content=[bin(x)[2:] for x in content]
                    content = memoryview(content)
                    packaging_info = content[:44]
                    raw_bytes = content[44:]
                self.directory_manager.add_folder(filename, [packaging_info, raw_bytes, str(bin(1)[2:])], address, path)
            elif extension=='.exe':
                with open(file_path, 'rb') as file:
                    content=bytearray(file.read())
                    content=memoryview(content)
                    packaging_info=content[:64]
                    raw_bytes=content[:64]
                self.directory_manager.add_folder(filename, [file_path, packaging_info, raw_bytes, str(bin(2)[2:])], address, path)
    """
    PACKAGING TYPE FOR TXT/
    data, extension
    
    PACKAGING TYPE FOR WAV/
    Packaging, data, extension
    """
    def run_slots(self,process_name:str = None, file_name:str = None, process_extensions:str = 'txt', disk_address:int = None):
        if process_name is not None:
            next_process_to_run=self.directory_manager.locate_object(process_name)
            print(next_process_to_run)
            if process_extensions =='.txt': #TODO fix for no file_name extensions
                self.exec_txt(file_name, process_name)
            elif process_extensions=='.wav':
                self.exec_wav(file_name, process_name)
            elif process_extensions=='.exe':
                #self.exec_exe(file_path=fil)
                pass
            if self.auto_migrate:
                if not disk_address:
                    free_space: list[int] = self.directory_manager.free_disk_space()
                    self.directory_manager.store_value(process_name,free_space[0])
                    self.directory_manager.delete_slots(next_process_to_run)
                elif disk_address:
                    self.directory_manager.store_value(process_name,disk_address)
                    self.directory_manager.delete_slots(next_process_to_run)
            self.scheduler_manager.mark_as_active(next_process_to_run)
        else:
            address = self.process_to_run() #TODO manage extensions for None process_name
            self.directory_manager.delete_slots(address)

    def allocate_area(self, start: int, end: int, area_name: str):
        area_list = []      #acts like set but is mutable to start (TODO: implement exclusion cases for set)
        for i in range(start, end+1):
            area_list.append(i)
        self.pcb_manager.area_allocation(set(area_list), area_name)


    def populate_status(self):
        print(self.scheduler_manager.populate_status())
        return self.scheduler_manager.populate_status()

    def output_pop(self):
        print(self.scheduler_manager.status)

    def loop_status(self):
        while self.populate_status():
            print("running")
            self.populate_status()

    def exec_pointers(self, subfile_name:str = None, disk_address:int=None,):
        pointers=list(list(self.directory_manager.pointers.values()))
        print(pointers)
        for i, v in enumerate(pointers):
            index_ram=pointers[i][0][0]
            ProcessName = self.ram[index_ram][0][2]
            if v!=0:
                DictLen=len(list(self.ram[index_ram][1].values()))-1
                data = list(self.ram[index_ram][1].values())[DictLen][-2]
                extension=list(self.ram[index_ram][1].values())[DictLen][-1]
                print(data)
                headers=list(self.ram[index_ram][1].keys())
                for j,k in enumerate(headers):
                    if extension==str(bin(0))[2:]:
                        t1 = threading.Thread(target=self.exec_txt, args=(k,ProcessName))
                        t1.start()
                    elif extension==str(bin(1))[2:]: #DONE
                        t1 = threading.Thread(target=self.exec_wav, args=(k, ProcessName))
                        t1.start()
                    elif extension==str(bin(2))[2:]: #DONE
                        if subfile_name:
                            t1 = threading.Thread(target=self.exec_exe,
                                                  args=(list(self.ram[index_ram][1].values())[DictLen][-4], index_ram, subfile_name))
                            t1.start()
                        else:
                            t1 = threading.Thread(target=self.exec_exe,
                                                  args=(list(self.ram[index_ram][1].values())[DictLen][-4], index_ram))
                            t1.start()
                            t1.join(timeout=1)
                            self.migrate_host_ram(subfile_name, '.txt', 'opened_file', index_ram)
                    else:
                        print("File not executable")
            if self.auto_migrate:
                if not disk_address:
                    free_space: list[int] = self.directory_manager.free_disk_space()
                    self.directory_manager.store_value(ProcessName,free_space[0])
                    self.directory_manager.delete_slots(index_ram)
                elif disk_address:
                    self.directory_manager.store_value(ProcessName,disk_address)
                    self.directory_manager.delete_slots(index_ram)
            self.scheduler_manager.mark_as_active(index_ram)
