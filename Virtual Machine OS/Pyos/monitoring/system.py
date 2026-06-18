import logging

import psutil
import threading
import keyboard
import time

class System:
    def __init__(self, max_power, process_manager=None):
        self.cpu_usage=0
        self.running_threads=0
        self.max_power=max_power
        self.process_manager = process_manager
        self.thread_id={}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        print(f"{threading.active_count()} active threads at init")

    def get_cpu(self, bootcode):
        if bootcode!='f00135b':
            return
        while True:
            try:
                self.cpu_usage=psutil.cpu_percent(interval=1)
                if self.cpu_usage>self.max_power:
                    self.pause_all_threads()
                    self.thread_id['0x006']=0
                    raise OverclockError(f"CPU usage at {self.cpu_usage}% caused early backfire. Sleeping for one second...")
                else:
                    self.thread_id = dict.fromkeys(self.thread_id, 1)
                self.running_threads=threading.active_count()
            except OverclockError as e:
                self.logger.error(f"Cpu usage spiked and caused an overclock."
                      f"Current threads: {self.running_threads}"
                      f"Current Cpu usage: {self.cpu_usage}", exc_info=True)
                time.sleep(0.5)
                self.process_manager.aut_update_thread()
                continue


    def run_diagnostic(self):
        self.create_thread_id("0x001")
        t1 = threading.Thread(target=self.get_cpu, args=('f00135b', ))
        t1.start()

    def set_thread_positive(self, id:str):
        self.thread_id[id]=1

    def delete_thread(self, id:str):
        self.thread_id.pop(id, None)
        print(self.thread_id)
    def create_thread_id(self, threader:str):
        self.thread_id[threader]=1
        print(self.thread_id)

    def pause_threads(self, threader:str):
        self.thread_id[threader]=0

    def pause_all_threads(self):
        self.thread_id = dict.fromkeys(self.thread_id, 0)

class OverclockError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("OverclockError occurred")
        time.sleep(1)
