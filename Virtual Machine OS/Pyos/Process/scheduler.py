from Tools.scripts.fixnotice import process


class Scheduler:
    def __init__(self, ram, directory_manager):
        self.ram = ram
        self.directory_manager = directory_manager
        self.schedule_processes = []

    def schedule_process_all(self):
        processes = list(self.directory_manager.give_filename_index())
        return processes

    def process_to_run(self):
        return self.schedule_process_all()[0]


