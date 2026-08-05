import time
import threading
import logging

class Scheduler:
    def __init__(self, ram, directory_manager, system_manager=None):
        self.ram = ram
        self.directory_manager = directory_manager
        self.system_manager=system_manager
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.propagate=False
        self.schedlog = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        handler = logging.FileHandler("TameOSschedlog.log", mode='w')
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.schedlog.addHandler(handler)
        self.schedlog.propagate = False
        self.schedule_processes = []
        self.ready_queue = []
        self.waiting_queue = []
        self.status={}
        self.file_timestamp:dict[int, dict[str, float]]={}

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

    def is_active(self, address:int):
        if address==0: #TODO fix for default allocated process area (DAPA)
            return True
        if self.status[address]==[0]:
            return False

    def full_status_list(self):
        print(self.status)
        return self.status

    def track_files_timestamp_thread(self, thread_code: str) ->None:
        """
        threading.Thread target function, tracking file longevity across the board.
        :param thread_code: boolean value
        :return: None
        """
        while True:
            if not self.system_manager.thread_id[thread_code]==1:
                continue
            for i in range(len(self.ram)):
                v = self.ram[i]
                if i==1024:
                    continue #Code seems to break if I don't do this... oh well let's hope slot 1024 doesn't magically appear at some point
                if v==0:
                    if i in self.file_timestamp.keys():
                        self.file_timestamp.pop(i)
                    continue
                if i not in self.file_timestamp.keys():
                    self.file_timestamp[i]={}
                    self.file_timestamp[i]['start_time']=time.time()
                self.file_timestamp[i]['current_time']=time.time()
            self.schedlog.info(self.file_timestamp)
            time.sleep(1)
    def track_files_timestamp(self):
        """
        Thread started for thread 0x009
        :return: None
        """
        thread_name="0x009"
        self.system_manager.create_thread_id(thread_name)
        self.logger.info(f"Started thread {thread_name} for setting and updating time stamps on running processes in RAM")
        t1 = threading.Thread(target=self.track_files_timestamp_thread, args=(thread_name, ))
        t1.start()

