from scheduler import Scheduler
from PCB import PCB
from pathlib import Path

class Manager:
    def __init__(self, ram, directory_manager):
        self.ram = ram
        self.directory_manager = directory_manager
        self.scheduler_manager = Scheduler(ram, directory_manager)
        self.pcb_manager = PCB(ram, directory_manager)

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

    def migrate_host_ram(self, path:str, extension:str, filename:str, address:int):
        file_path = Path(f"C:/Users/pasca/Downloads/{path}{extension}")
        if file_path.exists():
            with open(file_path, 'r') as file:
                content = list(file.read())
                content=[bin(ord(x))[2:] for x in content]
            self.directory_manager.add_folder(filename, content, address, path)


    def run_slots(self,file_name:str = None, process_extensions:str = 'txt', process_name:str = None):
        if process_name is not None:
            next_process_to_run=self.directory_manager.locate_object(process_name)
            print(next_process_to_run)
            if process_extensions =='.txt': #TODO fix for no file_name extensions
                decrypt=[]
                data = list(self.ram[next_process_to_run][1][file_name])
                for i in range(len(data)):
                    decrypt.append(chr(int(data[i], 2)))
                print("".join(x for x in decrypt))
            if process_extensions=='.wav':
                print("file extension not supported yet")
            self.directory_manager.delete_slots(next_process_to_run)
        else:
            address = self.process_to_run() #TODO manage extensions for None process_name
            self.directory_manager.delete_slots(address)

    def allocate_area(self, start: int, end: int, area_name: str):
        area_list = []      #acts like set but is mutable to start (TODO: implement exclusion cases for set)
        for i in range(start, end+1):
            area_list.append(i)
        self.pcb_manager.area_allocation(set(area_list), area_name)





