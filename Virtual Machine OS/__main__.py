from Tools.scripts.fixnotice import process

from manager import Manager
from ram import RAM
from filesystem import FileSystem
from directory import Directory
from PCB import PCB
from storage import Storage
from scheduler import Scheduler

ram=RAM(16)
storage=Storage(ram)
file_manager=FileSystem(ram, storage)
directory_manager=Directory(ram,  storage)
pcb_manager=PCB(ram, directory_manager)
scheduler_manager=Scheduler(ram, directory_manager)
process_manager=Manager(ram, directory_manager)


directory_manager.add_empty_folder('test1', [1,45,988,77,4], 0)
directory_manager.add_empty_folder('test2', [5,8,9,4,4], 6)
directory_manager.add_empty_folder('test3', [5,8,9,4,4], 5)
directory_manager.add_folder('test4', [5,6,4,8], 2, 'file1')
directory_manager.edit_file('test4', [51,3,4], 'file_test')
print(ram)
pcb_manager.track_inactivity()
print(ram)
directory_manager.store_value('test4', 13)
print(storage)
directory_manager.delete_folder_data('test4')
pcb_manager.track_inactivity()
print(ram)
pcb_manager.delete_inactive_slots()
print(ram)
directory_manager.add_folder('test5', [5,6,4,8], 2, 'file1')
print(storage)
directory_manager.migrate_storage_ram(4, 'test4')
print(ram)
process_manager.process_to_run()
process_manager.schedule_process_all()
process_manager.delete_inactive_slots()
print(ram)
process_manager.run_slots()
print(ram)
process_manager.allocate_area(4, 13, 'TestArea')
process_manager.allocate_area(2, 11, 'TestArea2')
directory_manager.update_PID()
print(ram)
directory_manager.reestablish_PID()
print(ram)