from repl import TameShell
from ram import RAM
from storage import Storage
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="TameOSlog.log", filemode='w',
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ram=RAM(1024)
    storage=Storage(ram)
    shell = TameShell(ram, storage)
    shell.loop()