import sys

from repl import TameShell
from ram import RAM
from storage import Storage
import logging

def main():
    logging.basicConfig(level=logging.INFO, filename="TameOSlog.log", filemode='w',
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(stdout_handler)
    ram = RAM(1024)
    storage = Storage(ram)
    shell = TameShell(ram, storage)
    shell.loop()
if __name__ == "__main__":
    main()
