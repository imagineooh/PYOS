from scheduler import Scheduler
from PCB import PCB

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

    def run_slots(self):
        next_process_to_run=self.process_to_run()
        self.directory_manager.delete_slots(next_process_to_run)

    def allocate_area(self, start: int, end: int, area_name: str):
        area_list = []      #acts like set but is mutable to start (TODO: implement exclusion cases for set)
        for i in range(start, end+1):
            area_list.append(i)
        self.pcb_manager.area_allocation(set(area_list), area_name)





