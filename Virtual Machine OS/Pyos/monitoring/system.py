import psutil
import threading
import keyboard
import time

class System:
    def __init__(self, max_power):
        self.cpu_usage=0
        self.running_threads=0
        self.max_power=max_power
        self.thread_id={}

    def get_cpu(self, bootcode):
        if bootcode!='f00135b':
            return
        while True:
            self.cpu_usage=psutil.cpu_percent(interval=1)
            if self.cpu_usage>self.max_power:
                self.pause_all_threads()
                raise OverclockError(f"CPU usage at {self.cpu_usage}% caused early backfire. Sleeping for one second...")
            else:
                self.thread_id = dict.fromkeys(self.thread_id, 1)
            self.running_threads=threading.active_count()

    def run_diagnostic(self):
        self.create_thread_id("0x001")
        t1 = threading.Thread(target=self.get_cpu, args=('f00135b', ))
        t1.start()

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
        time.sleep(1)
