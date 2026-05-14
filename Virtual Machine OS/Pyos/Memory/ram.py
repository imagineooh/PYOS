"""
This code is intended to provide a RAM like structure that enables safe communication between any type of computer systems
Progress is still underway.
This is not necessarlay computer RAM, but my project is to build a VIM for an OS entierely in python.
"""
class RAM:
    def __init__(self,
                 size: int,
                 backup_pointers_count = 0,
                 data=None,
                 backup=None,
                 freesd=None,
                 users=None,
                 pointers=None,
                 pointers_backup = None
                 ):

        self.size = size
        self.backup_pointers_count=backup_pointers_count
        self.data = data if data is not None else [0] * size
        self.backup = backup if backup is not None else [0] * size  # backup used to store data that is out of bounds of the RAM, making it hidden ram (or HRAM)
        self.freesd = freesd if freesd is not None else []  # freesd used to store data that is freed, making it free space (or FS)
        self.users = users if users is not None else {}
        self.pointers = pointers if pointers is not None else []
        self.pointers_backup = pointers_backup if pointers_backup is not None else {}
    #END OF __INIT__

    def __hash__(self):
        return hash(self.backup_pointers_count)

    def __getitem__(self, item):
        if self.auth:
            if item< len(self.data):
                return self.data[item]
            else:
                print('Data out of bounds')
    def __setitem__(self, address, value):
        if self.auth():
            if address<len(self.data):
                self.data[address]=value
            else:
                print("Data out of bounds")



    def sign_in(self, username: str, password: str):
        self.password = password
        self.username = username

    def __str__(self):
        if self.auth():
            return f"RAM(size={self.size}, data={self.data})"
        else:
            return f"You do not have access to this active memory"

    def add_user(self, user, code):
        self.users[user] = code

    def auth(self) -> bool:
        if self.username in self.users:
            if self.users[self.username] == self.password:
                return True
            else:
                print("Access Denied")
                return False
        elif self.username is None:
            print("Please sign in with 'sign_in' method")
        else:
            print("No such username, create account with 'create' Method")
            return False

    def read_index(self, adress):
        if self.auth():
            if adress < self.size:
                print(self.data[adress])
                return self.data[adress]
            else:
                print(f"Data out of bounds for index {adress}")

    def write_int(self, adress: int, value: int):
        if self.auth():
            if adress < self.size:
                if self.data[adress]==0:
                    self.data[adress] = bin(value)
                else:
                    print(f"Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//") #TODO: Fix for file case
            else:
                print(f"Data out of bounds for index {adress}. " \
                      "If you wish to force write the value to RAM (unsafe), use 'force_writee' method.")
                self.backup[int(adress - len(self.data))] = bin(value)

    def write(self, address: int, value, bypass:bool):
        if self.auth():
            if address < self.size:
                if self.data[address]==0:
                    self.data[address] = value
                elif not bypass:
                    print(f"Data adress already taken, try 'force_write' method (unsafe) or 'free_index' method first. ...//")
                elif bypass:
                    print("Bypassing restriction for folder allocation")
            else:
                print(f"Data out of bounds for index {address}. " \
                      "If you wish to force write the value to RAM (unsafe), use 'force_writee' method.")
                self.backup[address - self.size] = bin(value)

    def free_index(self, adress:int):
        if self.auth() and input(f"Clearing would result in deleting value {self.data[adress]} from system. Do you with to proceed (y/n)? ...//")=='y':
            self.data[adress]=0

    def read(self) -> None:
        if self.auth():
            print(self.data)
            return self.data

    def clear(self) -> None:
        if self.auth():
            self.data = [0] * self.size

    def is_taken(self, adress:int) -> bool:
        if self.auth():
            if adress < self.size:
                print(self.data[adress] != 0)
                return self.data[adress] != 0
            else:
                print(f"Data out of bounds for index {adress}")

    def index_free(self):
        if self.auth():
            self.freesd = []
            for i in range(self.size):
                if self.data[i] == 0:
                    self.freesd.append(i)
            print(
                f'Free space situated at indeces: { ", ".join(str(x) for x in self.freesd)}; ({len(self.freesd)} free slots total)')
            return self.freesd

    def point_to(self, imported: list[int]):  # when the pointer list is updated, all previous elements are deleted
        if self.auth():
            for i in range (1, len(self.pointers)+1):
                self.backup_pointers_count += 1
                self.pointers_backup[f"@{self.backup_pointers_count}"] = self.pointers[len(self.pointers)-i] #pointer adress format: @pos
            self.pointers=[]
            for i in range(len(imported)):
                if imported[i] <= len(self.data):
                    self.pointers.append(imported[i])
            """while len(imported) < len(self.pointers):
                self.backup_pointers_count +=1
                self.pointers_backup[self.backup_pointers_count]=self.pointers[-1]
                del self.pointers[-1]"""
            print(self.pointers_backup)

    def view_multiple(self):
        if self.auth():
            temp = []
            if len(self.pointers) > 0:
                for i in range(len(self.pointers)):
                    temp.append(self.data[self.pointers[i]])
                print(", ".join(str(x) for x in temp))
                return temp
            else:
                print("No pointers in system, could not read multiple indeces. Try " \
                      "adding pointers with 'point_to' method, " \
                      "or try reading single values with 'read_index' method.")

    def view_multiple_from_old(self):
        if self.auth():
            if len(self.pointers_backup)>0:
                temp=[]
                for i in range(1,len(self.pointers_backup)+1):
                    temp.append(self.data[self.pointers_backup[f"@{i}"]])
                print(", ".join(str(x) for x in temp))
                return temp
            else:
                print("No old pointers in sytem...//")

    def force_write(self, adress: int, value:int):
        if self.auth():
            if adress>len(self.data):
                if input("This method is unsafe as it will take more space in RAM. Do you wish to proceed? (y/n) ...//")=='y':
                    while len(self.data)<(adress-1):
                        self.data.append(0)
                    if len(self.data)==(adress-1):
                        self.data.append(value)
            if self.data[adress]!=0:
                self.data[adress]=value

    def add_file(self, address: int, file_name: str):
        if self.auth():
            if address<self.size:
                hashmap={file_name: 0}
                self.data.insert(address, hashmap)

    def return_size(self):
        return len(self.data)


    def len_RAM(self):
        return len(self.data)