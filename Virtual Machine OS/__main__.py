from ram import RAM
from filesystem import FileSystem


ram=RAM(16)
file_manager=FileSystem(ram)


file_manager.construct_folder('test',[1,5,6], 5)
file_manager.construct_folder('test2', [1,6,1,5,7,9,8,4], 6)
print(ram)
