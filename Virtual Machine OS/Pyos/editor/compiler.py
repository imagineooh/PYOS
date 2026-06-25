import re

class Compiler:
    def __init__(self, ram = None, directory_manager= None, inputed_file:str=None):
        self.ram = ram
        self.directory_manager = directory_manager
        self.file = None
        self.lines = None
        self.operating_functions = {
            "+": lambda x, y: [str(x+y)],
            "-": lambda x, y: [str(x - y)],
            "/": lambda x, y: [str(x / y)],
            "*": lambda x, y: [str(x * y)]
        }
        self.mapper = {
            "SET":self.__do_set,
            "OP":self.__do_op,
        }
        self.variable_status={}

    def compile(self, inputed_file: str = None):
        """
        Main function for compiler, only public function that can be used outside
        :return:
        """
        if inputed_file is not None:
            with open(inputed_file, 'r') as file:
                self.lines:list = [line.strip() for line in file]
        else:
            #self.lines: list = ["OP 2*3-2", "OP 12*456-2", "OP ((237232/4544-2*5)+2)/4"]
            self.lines: list = ["SET x=3*(12*4*(5-6))-(18*(4+2))/5"]
        for i,value in enumerate(self.lines):
            keyword = value.split()[0]
            self.mapper[keyword](i, len(keyword))


    def __do_set(self, line_number:str, keyword_len:int = 3):
        line = self.lines[line_number]
        body = line[keyword_len:]
        tokens = body.split("=", 1)
        variable_name = tokens[0].strip()
        self.variable_status[variable_name] = "const"
        #variable_expression = tokens[1].strip()
        offset = keyword_len + len(variable_name)+2
        #print(f"offsetted to {line[offset:]}")
        variable_value = self.__do_op(line_number, offset)
        #self.directory_manager.add_empty_folder(variable_name, variable_value, 0)
        print(f"{variable_name} = {variable_value}")

    def __do_op(self, line_number:str, keyword_len:int = 2):
        line = self.lines[line_number]
        print("evaluating line", line)
        body = re.findall(r'\d+|[\+\-\*/\(\)]',line[keyword_len:])
        special_charaters=['(',')']

        true_len=len(body)
        for k in range(true_len):
            try:
                for i, value in enumerate(body):
                    if body[i-1] in special_charaters or body[i+1] in special_charaters:
                        body = self.__run_clause(body, special_charaters)
                        print(body)
                        continue
                    if value=='*' or value == "/":
                        body[i-1:i+2] = self.operating_functions[value](float(body[i - 1]), float(body[i + 1]))
                        print(body)
                        break
                for i, value in enumerate(body):
                    if body[i-1] in special_charaters or body[i+1] in special_charaters:
                        body = self.__run_clause(body, special_charaters)
                        print(body)
                        continue
                    if value=='+' or value == "-":
                        if i+2<len(body) and i-1>0:
                            if body[i-2] == "*" or body[i+2]=="*":
                                continue
                            if body[i-2] == "/" or body[i+2]=="/":
                                continue
                        else:
                            if body[i-2] == "*":
                                continue
                            if body[i-2] == "/":
                                continue
                        body[i - 1:i + 2] = self.operating_functions[value](float(body[i - 1]), float(body[i + 1]))
                        print(body)
                        break
            except ValueError:
                if body[k] in special_charaters:
                    body.pop(k)
            except IndexError:
                continue
        body = [x for x in body if x not in special_charaters]
        for _ in range(len(body)):
            for i, value in enumerate(body):
                if value == '*' or value == "/":
                    body[i - 1:i + 2] = self.operating_functions[value](float(body[i - 1]), float(body[i + 1]))
                    break
            for i, value in enumerate(body):
                if value == '+' or value == "-":
                    body[i - 1:i + 2] = self.operating_functions[value](float(body[i - 1]), float(body[i + 1]))
                    break
        result = float(body[0])
        return result

    @staticmethod
    def __run_clause(body:list, spec:list):
        new_body  = list(body)
        for _ in range(len(body)):
            for i, v in enumerate(new_body):
                if not v in spec:

                    break
                if new_body[i+2] in spec and i+2<len(new_body):
                    new_body.pop(i)
                    real_len = len(new_body)

                    break
                elif new_body[i+2] in spec and new_body[i+2]!=v:
                    new_body.pop(i)
                    new_body.pop(i+2)
                    real_len = len(new_body)

                    break
                
        return new_body
bas_comp = Compiler()
bas_comp.compile()

