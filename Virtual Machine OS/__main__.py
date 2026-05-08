from ram import RAM
from filesystem import FileSystem
from directory import Directory

ram=RAM(16)
file_manager=FileSystem(ram)
directory_manager=Directory(ram)

directory_manager.add_empty_folder('test', [1,45,988,77,4], 5)
directory_manager.add_empty_folder('test2', [5,8,9,4,4], 6)
directory_manager.add_empty_folder('test3', [5,8,9,4,4], 5)
print(ram)

