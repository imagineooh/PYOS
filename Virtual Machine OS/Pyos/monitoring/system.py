import psutil
import threading
import keyboard
import time

class System:
    def __init__(self, max_power):
        self.cpu_usage=0
        self.running_threads=0
        self.max_power=max_power
    def get_cpu(self, bootcode):
        if bootcode!='f00135b':
            return
        while True:
            self.cpu_usage=psutil.cpu_percent(interval=1)
            if self.cpu_usage>self.max_power:
                raise OverclockError(f"CPU usage at {self.cpu_usage} caused early backfire")
            self.running_threads=threading.active_count()

    def run_diagnostic(self):
        t1 = threading.Thread(target=self.get_cpu, args=('f00135b', ))
        t1.start()

class OverclockError(Exception):
    def __init__(self, message):
        super().__init__(message)
        time.sleep(1)
