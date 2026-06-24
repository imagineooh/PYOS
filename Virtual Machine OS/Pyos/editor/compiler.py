class Compiler:
    def __init__(self, ram, directory_manager, inputed_file:str=None):
        self.ram = ram
        self.directory_manager = directory_manager
        self.file = None
        self.lines = None
        self.mapper = {
            "SET":self.__do_set,
        }

    def compile(self, inputed_file: str):
        """
        Main function for compiler, only public function that can be used outside
        :return:
        """
        with open(inputed_file, 'r') as file:
            self.lines = [line.strip() for line in file]
        for i,value in enumerate(self.lines):
            keyword = value.split()[0]


    def __do_set(self, line_number:str, keyword_len:int = 3):
        line = self.lines[line_number]
        body = line[keyword_len:]
        tokens = body.split("=", 1)
        variable_name = tokens[0].strip()
        variable_value = body[1]
        self.directory_manager.add_empty_folder(variable_name, variable_value, 0)