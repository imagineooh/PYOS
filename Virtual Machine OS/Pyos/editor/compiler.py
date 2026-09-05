"""
Lowest level language that TameOS can understand, called TameScript (or TASM), this is the
equivalent of an assembly language for a regular OS.

Is higher level than most ASM, as scope is directly taken care of without the user needing to manually add to stack.
For functions or loops, jumps and conditionals are still required.

For any inquiries, or if someone wants to make a higher level language that compiles to TameOS, please start
a discussion on the discussion tab.

I am working on a simple way to add addon languages to compile to TameScript.
"""



import re
import logging

class CustomExceptionHandler:
    logger = logging.getLogger(f"{__name__}.compiler")
    handler = logging.FileHandler("CompilerOutput.log", mode='w')
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    new_handler = logging.FileHandler("CompilerOutput.txt", mode='w')
    logger.addHandler(new_handler)
    logger.propagate = False
    def __init__(self):
        pass
    @classmethod
    def raiseerror(cls, message, line_number):
        cls.logger.info(f"{cls.__name__} \n Error on line {line_number}: '{message}'")

class ConstChangeError(CustomExceptionHandler):
    def __init__(self):
        super().__init__()

class NonExistentError(CustomExceptionHandler):
    def __init__(self):
        super().__init__()

class Compiler:
    def __init__(self, errhand, ram, directory_manager, inputed_file:str=None):
        self.current = 0
        self.ram = ram
        self.directory_manager = directory_manager
        self.error_handler = errhand
        self.logger = logger = logging.getLogger(f"{__name__}.compiler")
        new_handler = logging.FileHandler("CompilerOutput.txt", mode='w')
        self.logger.addHandler(new_handler)
        self.logger.propagate = False
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
            "JMP":self.__jump,
            "JPU": self.__jumpu,
            "STDOUT": self.__stdout
        }
        self.variable_status={}
        self.all_ops= {"+": 1,
                       "-": 1,
                       "*": 2,
                       "/":2,
                       }
        self.local_setting:bool = False
        self.checked=[]
        self.active = True
        self.injump = False


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
            self.lines: list = ["SET x=3*(-12*4*(5- 6))-(18*(4+2))/5",
                                "SET i=0",
                                "SET x=5",
                                "SET y = 7",
                                "SET i = i+1",
                                "JPU 2 i 6",
                                "VOID {",
                                "SET z = 546",
                                "SET j = hello",
                                "}",
                                "SET y = x + 5",
                                "STDOUT y"
                                ]
        self.current=0
        while self.active:
            value=self.lines[self.current]
            """if self.current in self.checked:
                continue"""
            keyword = value.split()[0]
            if keyword not in self.mapper.keys():
                continue
            self.mapper[keyword](self.current, len(keyword))
            #self.checked.append(self.current)
            if self.current==len(self.lines)-1:
                self.active = False
                break
            self.current+=1


    def __stdout(self, line_number, keyword_len):
        token = self.lines[line_number][keyword_len:].strip()
        if self.directory_manager.locate_object(token):
            address = self.directory_manager.locate_object(token)
            body = self.ram[address][1]['value']
            self.logger.info(body)
        else:
            NonExistentError.raiseerror(f"Variable {token} does not exist")

    def __set_local(self, line_number:int, keyword_len:int = 4):
        #print(f"FOUND LINE NUMBER{line_number}")
        local_lines = self.lines[line_number+1:]
        self.local_setting = True
        for i, v in enumerate(local_lines):
            self.checked.append(i+line_number+1)
            if v == "}":
                self.local_setting = False
                self.directory_manager.free_heap()
                self.current+=1
                break
            if not self.local_setting:
                break
            keyword = v.split()[0]
            self.current += 1
            self.mapper[keyword](self.current, len(keyword))

    def __jump(self, curline:int, lk):
        jmpat = int(self.lines[curline][lk:].strip())
        self.current=jmpat-1
        """for i in range(self.current, len(self.checked)):
            self.checked.pop(i)"""

    def __jumpu(self, curline:int, lk):
        """
        Jump when a variable is under a value
        :param curline: Current working line
        :param lk: keyword length
        :return: line number
        """
        bodysplit = self.lines[curline][lk:].split()
        jumpat=int(bodysplit[0])
        token = bodysplit[1]
        if self.directory_manager.file_exists(token):
            token_address = self.directory_manager.locate_object(token)
            var_conditional = int(self.ram[token_address][1]["value"])
        upper_limit = int(bodysplit[2])
        if var_conditional is None:
            NonExistentError.raiseerror(f"Conditional variable {token} does not exist", curline)
            return None
        if var_conditional<upper_limit:
            self.current=jumpat-1

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
        if self.directory_manager.file_exists(tokens[1].strip()):
            token_address = self.directory_manager.locate_object(tokens[1].strip())
            variable_value = self.ram[token_address][1]["value"]
        else:
            variable_value = self.__do_op(line_number, offset)
        if self.local_setting:
            commit_address = self.directory_manager.vfree_spot(local = True)
        else:
            commit_address = self.directory_manager.vfree_spot(local = False)
        var_hash = hash(variable_value)
        """print(variable_name)
        print(variable_value)"""
        self.directory_manager.protect_slot(commit_address)
        self.directory_manager.add_variable(variable_name, variable_value, commit_address, hash_value=var_hash, var_type = prevar_stat)




    def __do_op(self, line_number: str, keyword_len: int = 2):
        line = self.lines[line_number]
        body_first = line[keyword_len:]
        body = list(re.findall(r'-?\d+|[a-zA-Z]+|[\+\-\*/\(\)]', body_first))
        for i, token in enumerate(body):
            if self.directory_manager.file_exists(token):
                token_address = self.directory_manager.locate_object(token)
                body[i] = self.ram[token_address][1]["value"]
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




