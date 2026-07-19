import re


class CustomExceptionHandler:
    def __init__(self):
        pass
    @classmethod
    def raiseerror(cls, message, line_number):
        print(f"{cls.__name__} \n Error on line {line_number}: '{message}'")

class ConstChangeError(CustomExceptionHandler):
    def __init__(self):
        super().__init__()

class Compiler:

    def __init__(self, errhand, ram, directory_manager, inputed_file:str=None):
        self.ram = ram
        self.directory_manager = directory_manager
        self.error_handler = errhand
        self.file = None
        self.lines = None
        self.operating_functions = {
            "+": lambda x, y: float(x+y),
            "-": lambda x, y: float(x - y),
            "/": lambda x, y: float(x / y),
            "*": lambda x, y: float(x * y)
        }
        self.mapper = {
            "SET":self.__do_set,
            "CONST": self.__do_set,
            "OP":self.__do_op,
            "VOID": self.__set_local,
        }
        self.variable_status={}
        self.all_ops= {"+": 1,
                       "-": 1,
                       "*": 2,
                       "/":2,
                       }
        self.local_setting:bool = False
        self.checked=[]


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
            self.lines: list = ["CONST x=3*(-12*4*(5- 6))-(18*(4+2))/5",
                                "CONST x=5",
                                "SET y = 7",
                                "VOID {",
                                "SET z = 8",
                                "SET j = hello",
                                "}",
                                "SET y=10"]
        for i,value in enumerate(self.lines):
            if i in self.checked:
                continue
            keyword = value.split()[0]
            if keyword not in self.mapper.keys():
                continue
            self.mapper[keyword](i, len(keyword))
            self.checked.append(i)

    def __set_local(self, line_number:int, keyword_len:int = 4):
        print(f"FOUND LINE NUMBER{line_number}")
        local_lines = self.lines[line_number+1:]
        self.local_setting = True
        for i, v in enumerate(local_lines):
            self.checked.append(i+line_number+1)
            if v == "}":
                self.local_setting = False
                self.directory_manager.free_heap()
                break
            keyword = v.split()[0]
            self.mapper[keyword](i+line_number+1, len(keyword))

    def __do_set(self, line_number:int, keyword_len:int = 3) ->None:
        """
        Hidden setter method for adding variable in memory from compiler
        :param line_number: str, line read for setting
        :param keyword_len: len of the keyword arg
        :return: None
        """
        line = self.lines[line_number]
        body = line[keyword_len:]
        tokens = body.split("=")
        """try:
            tester = int(tokens[1])
        except TypeError:
            return tokens[1]"""
        variable_name = tokens[0].strip()
        if variable_name in self.variable_status.keys():
            if self.variable_status[variable_name]=="const":
                ConstChangeError.raiseerror(message=body, line_number=line_number)
                return
            else:
                prevar_stat = "var"
        else:
            prevar_stat = "var"
        keyword=line[:keyword_len]
        if keyword=="CONST":
            self.variable_status[variable_name] = "const"
        else:
            self.variable_status[variable_name] = "var"
        offset = keyword_len + len(variable_name)+2
        variable_value = self.__do_op(line_number, offset)
        if self.local_setting:
            commit_address = self.directory_manager.vfree_spot(local = True)
        else:
            commit_address = self.directory_manager.vfree_spot(local = False)
        self.directory_manager.add_variable(variable_name, variable_value, commit_address, var_type = prevar_stat)




    def __do_op(self, line_number: str, keyword_len: int = 2):
        line = self.lines[line_number]
        body_first = line[keyword_len:]
        body = list(re.findall(r'-?\d+|[\+\-\*/\(\)]', body_first))
        if len(body)==0:
            return body_first.split("=")[1].strip()
        """if len(body)==1:
            return body[0]"""
        proc= self.all_ops
        mapper = self.operating_functions
        op = []
        out = []
        prev = 0
        part = ["(", ")"]
        for token in body:
            if not token in proc.keys() and not token in part:
                out.append(token)
                continue
            if token == ')':
                while op and op[-1] != '(':
                    out.append(op.pop())
                if op:
                    op.pop()
                continue
            if token == '(':
                op.append(token)
                continue
            if proc[token] >= prev:
                op.append(token)
                prev = proc[token]
                continue
            elif proc[token] < prev:
                while op and op[-1] in proc.keys():
                    out.append(op.pop())
                op.append(token)
        if len(op)>0:
            for _ in range(len(op)):
                out.append(op.pop(-1))
        stack = []
        for i, v in enumerate(out):
            if v not in proc.keys():
                stack.append(v)
                continue
            result = mapper[v](float(stack[-2]), float(stack[-1]))
            stack.pop()
            stack.pop()
            stack.append(result)
        try:
            return float(stack[0])
        except ValueError:
            return stack[0]
        except IndexError:
            return body[0]

"""bas_comp = Compiler(CustomExceptionHandler)
bas_comp.compile()"""



