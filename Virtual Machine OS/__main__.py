from ram import RAM
from filesystem import FileSystem
from directory import Directory
from PCB import PCB
from storage import Storage

ram=RAM(16)
storage=Storage(ram)
file_manager=FileSystem(ram, storage)
directory_manager=Directory(ram,  storage)
pcb_manager=PCB(ram, directory_manager)

directory_manager.add_empty_folder('test1', [1,45,988,77,4], 5)
directory_manager.add_empty_folder('test2', [5,8,9,4,4], 6)
directory_manager.add_empty_folder('test3', [5,8,9,4,4], 5)
directory_manager.add_folder('test4', [5,6,4,8], 2, 'file1')
directory_manager.edit_file('test4', [51,3,4], 'file_test')
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
directory_manager.migrate_storage_ram(1, 'test4')
print(ram)




