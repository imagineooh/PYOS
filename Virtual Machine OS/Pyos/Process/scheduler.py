class Scheduler:
    def __init__(self, ram, directory_manager):
        self.ram = ram
        self.directory_manager = directory_manager
        self.schedule_processes = []
        self.ready_queue = []
        self.waiting_queue = []
        self.status={}

    def schedule_process_all(self):
        processes = list(self.directory_manager.give_filename_index())
        return processes

    def process_to_run(self):
        return self.schedule_process_all()[0]

    def add_to_ready(self):
        if len(self.ready_queue)<10:
            self.ready_queue.append(self.schedule_process_all()[0])
        else:
            self.add_to_waiting(self.schedule_process_all()[0])

    def add_to_waiting(self, value):
        self.waiting_queue.append(value)

    def delete_ready_value(self):
        self.ready_queue.pop(0)

    def populate_status(self):
        scheduled=self.schedule_process_all()
        for i in range(self.ram.len_RAM()):
            if self.ram[i]!=0:
                index = self.ram[i][0][0]
                if self.ram[i][1]!=0:
                    self.status[index]=[0]
                    self.status[index].append(scheduled.index(index))
                else:
                    self.status[index]=[-1]
        return self.status

    def mark_as_active(self, address:int):
        self.status[address]=[1,-1]

    def mark_as_inactive(self, address:int):
        self.status[address]=[0]
