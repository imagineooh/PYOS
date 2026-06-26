import re

class Compiler:
    def __init__(self, ram = None, directory_manager= None, inputed_file:str=None):
        self.ram = ram
        self.directory_manager = directory_manager
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
            "OP":self.__do_op,
        }
        self.variable_status={}
        self.all_ops= {"+": 1,
                       "-": 1,
                       "*": 2,
                       "/":2,
                       }


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



    def __do_op(self, line_number: str, keyword_len: int = 2):
        line = self.lines[line_number]
        body = line[keyword_len:]
        print(body)
        body = re.findall(r'\d+|[\+\-\*/\(\)]', body)
        operator_stack = []
        number_queue = []
        output_queue_ops=[]
        output_queue_val = []
        excluded = ['(', ')']
        for i, v in enumerate(body):
            all_ops_list = list(self.all_ops.keys())
            if i==0:
                if v in self.all_ops:
                    operator_stack.append(v)
                elif v not in self.all_ops and v not in excluded:
                    output_queue_val.append(v)
            else:
                if v not in all_ops_list and v not in excluded:
                    output_queue_val.append(v)
                    continue
                if len(operator_stack)>0:
                    if v == "(":
                        operator_stack.append(v)
                        continue
                    if v==")":
                        ctn = -1
                        for _ in range(len(operator_stack)):
                            if not operator_stack:
                                break
                            obj = operator_stack[ctn]
                            if obj == "(":
                                operator_stack.pop(ctn)
                                break
                            if obj!="(" and obj!=")":
                                output_queue_ops.append(obj)
                            operator_stack.pop(ctn)
                        continue
                    if v not in excluded:
                        if operator_stack[-1] in excluded:
                            operator_stack.append(v)
                            continue
                        if self.all_ops[v]>self.all_ops[operator_stack[-1]]:
                            operator_stack.append(v)
                        else:
                            #output_queue_ops.append(v)
                            while operator_stack:
                                if operator_stack[-1] in self.all_ops.keys():
                                    output_queue_ops.append(operator_stack[-1])
                                    operator_stack.pop(-1)
                                else:
                                    break
                            operator_stack.append(v)
                else:
                    operator_stack.append(v)

        print('op stack before end', operator_stack)
        while len(operator_stack)>0:
            output_queue_ops.append(operator_stack[-1])
            operator_stack.pop(-1)
        """final_output = list(output_queue_val)
        for i in range(len(output_queue_ops)):
            final_output.append(output_queue_ops[i])"""
        ops_counter=0
        final=0

        print(output_queue_val)
        print(output_queue_ops)

        """for i, v in enumerate(output_queue_val):
            if i+1<len(output_queue_val):
                final+=self.operating_functions[output_queue_ops[ops_counter]](float(v), float(output_queue_val[i+1]))
                print(final)
        print(final)"""
        #print(number_queue, operator_stack, output_queue_ops)




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

