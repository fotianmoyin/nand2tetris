import random
import string
from command_types import CommandTypes


class CodeWriter:
    """
    将VM命令翻译成Hack汇编代码
    """

    def __init__(self, asm_path: str) -> None:
        """
        打开输出文件/输出流，准备进行写入
        参数：
        asm_path(str)：asm汇编文件地址
        """
        self.asm_path = asm_path
        # asm指令缓存
        self.lines: list[str] = []
        # 标签序号
        self.label_index = 0
        # 当前vm文件名
        self.file_name: str = None
        # 是否为多vm文件编译
        self.multi_vm = False
        # 是否有Sys.init函数
        self.has_init = False
        # 当前编译的函数名
        self.function_name: str = None
        # 输出注释
        self.output_comment: bool = True
        pass

    def set_file_name(self, file_name: str):
        """
        通知代码写入程序，新的VM文件翻译过程已经开始
        参数：
        file_name(str)：vm文件名
        """
        self.file_name = file_name
        self.function_name = None
        pass

    def write_arithmetic(self, command: str):
        """
        将给定的算术操作所对应的汇编代码写至输出
        参数：
        command(str)：命令
        """
        self.add_comment(self.lines, f"// {command}")
        match command:
            case "add" | "sub" | "neg":
                # 整数操作
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                if command == "add":
                    self.lines.append("M=M+D")
                if command == "sub":
                    self.lines.append("M=M-D")
                if command == "neg":
                    self.lines.append("M=-M")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "eq" | "gt" | "lt":
                # 大小判断
                judge = command.upper()
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("D=M-D")
                judge_label = self.create_label(judge)
                self.lines.append(f"@{judge_label}")
                self.lines.append(f"D;J{judge}")
                self.lines.append("D=0")
                next_label = self.create_label("NEXT")
                self.lines.append(f"@{next_label}")
                self.lines.append("0;JMP")
                self.lines.append(f"({judge_label})")
                self.lines.append("D=-1")
                self.lines.append(f"({next_label})")
                self.lines.append("@SP")
                self.lines.append("A=M")
                self.lines.append("M=D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "and" | "or" | "not":
                # 位操作
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                if command == "and":
                    self.lines.append("M=M&D")
                if command == "or":
                    self.lines.append("M=M|D")
                if command == "not":
                    self.lines.append("M=!M")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
        pass

    def create_label(self, prefix: str) -> str:
        # 生成5位随即大写字母
        # label = "".join(random.sample(string.ascii_uppercase, 5))
        label = f"{self.file_name}.{prefix}_{self.label_index}"
        self.label_index = self.label_index + 1
        return label

    def write_push_pop(self, command_type: CommandTypes, segment: str, index: int):
        """
        将给定的command（命令类型为C_PUSH或C_POP）所对应的汇编代码写入至输出
        参数：
        command_type(CommandTypes)：命令类型
        segment(str)：内存段
        index(int)：内存段中内存单元索引
        """
        match segment:
            case "argument" | "local" | "this" | "that" | "temp":
                # argument：存储函数的参数
                # local：存储函数的局部变量
                # this：通用段，能够与堆中不同区域相对应来满足各种程序编写需求
                # that：能够与堆中不同区域相对应来满足各种程序编写需求
                # temp：固定的段，由8个内存单元组成，用来保存临时变量
                dics = {
                    "argument": "ARG",
                    "local": "LCL",
                    "this": "THIS",
                    "that": "THAT",
                    "temp": "R5",
                }
                alias = dics[segment]
                if command_type == CommandTypes.C_PUSH:
                    self.push_from_segment(alias, index, segment == "temp")
                else:
                    self.pop_to_segment(alias, index, segment == "temp")
                pass
            case "static":
                # 存储同一.vm文件中所有函数共享的静态变量
                if command_type == CommandTypes.C_PUSH:
                    self.add_comment(self.lines, f"// push static {index}")
                    self.lines.append(f"@{self.file_name}.{index}")
                    self.lines.append("D=M")
                    self.push_from_d()
                else:
                    self.add_comment(self.lines, f"// pop static {index}")
                    self.pop_to_d()
                    self.lines.append(f"@{self.file_name}.{index}")
                    self.lines.append("M=D")
                pass
            case "constant":
                # 包含所有常数的伪段，常数的范围为0...32767
                if command_type == CommandTypes.C_PUSH:
                    self.add_comment(self.lines, f"// push constant {index}")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=A")
                    self.push_from_d()
                pass
            case "pointer":
                # 该段由2个内存单元组成，用来保存this和that段的基地址，
                # 任何VM函数可以将pointer0（或1）设置到某一地址上，
                # 这相当于将this（或that）段联结到起始于该地址的堆区域上
                if command_type == CommandTypes.C_PUSH:
                    self.add_comment(self.lines, f"// push pointer {index}")
                    if index == 0:
                        self.lines.append("@THIS")
                    if index == 1:
                        self.lines.append("@THAT")
                    self.lines.append("D=M")
                    self.push_from_d()
                else:
                    self.add_comment(self.lines, f"// pop pointer {index}")
                    self.pop_to_d()
                    if index == 0:
                        self.lines.append("@THIS")
                    if index == 1:
                        self.lines.append("@THAT")
                    self.lines.append("M=D")
                pass
        pass

    def push_from_d(self):
        """
        将D寄存器的值进栈
        """
        self.lines.append("@SP")
        self.lines.append("A=M")
        self.lines.append("M=D")
        self.lines.append("@SP")
        self.lines.append("M=M+1")
        pass

    def push_from_segment(self, segment: str, index: int, use_a: bool):
        """
        将指定索引的段值进栈
        参数：
        segment(str)：段
        index(int)：段索引
        use_a(bool)：使用A寄存器的值还是对应RAM中的值
        """
        self.add_comment(self.lines, f"// push {segment} {index}")
        self.lines.append(f"@{segment}")
        if use_a:
            self.lines.append("D=A")
        else:
            self.lines.append("D=M")
        self.lines.append(f"@{index}")
        self.lines.append("D=D+A")
        self.lines.append("A=D")
        self.lines.append("D=M")
        self.push_from_d()
        pass

    def pop_to_d(self):
        """
        将栈弹出的值存到D寄存器
        """
        self.lines.append("@SP")
        self.lines.append("AM=M-1")
        self.lines.append("D=M")
        pass

    def pop_to_segment(self, segment: str, index: int, use_a: bool):
        """
        将栈弹出的值存到指定索引的段
        参数：
        segment(str)：段
        index(int)：段索引
        use_a(bool)：使用A寄存器的值还是对应RAM中的值
        """
        self.add_comment(self.lines, f"// pop {segment} {index}")
        self.lines.append(f"@{segment}")
        if use_a:
            self.lines.append("D=A")
        else:
            self.lines.append("D=M")
        self.lines.append(f"@{index}")
        self.lines.append("D=D+A")
        self.lines.append("@R13")
        self.lines.append("M=D")
        self.pop_to_d()
        self.lines.append("@R13")
        self.lines.append("A=M")
        self.lines.append("M=D")
        pass

    def write_init(self):
        """
        编写执行VM初始化的汇编代码，也称为引导程序代码，
        该代码必须被置于输出文件的开头
        """
        lines = self.build_call("Sys.init", 0)
        for i in range(len(lines)):
            self.lines.insert(i, lines[i])
        pass

    def write_label(self, label: str):
        """
        编写执行label命令的汇编代码
        """
        label_name = label
        if self.function_name != None:
            label_name = f"{self.function_name}${label}"
        self.lines.append(f"({label_name})")
        pass

    def write_goto(self, label: str):
        """
        编写执行goto命令的汇编代码
        """
        label_name = label
        if self.function_name != None:
            label_name = f"{self.function_name}${label}"
        self.add_comment(self.lines, f"// goto {label_name}")
        self.lines.append(f"@{label_name}")
        self.lines.append("0;JMP")
        pass

    def write_if(self, label: str):
        """
        编写执行if-goto命令的汇编代码
        """
        label_name = label
        if self.function_name != None:
            label_name = f"{self.function_name}${label}"
        self.add_comment(self.lines, f"// if-goto {label_name}")
        self.pop_to_d()
        self.lines.append(f"@{label_name}")
        self.lines.append("D;JNE")
        pass

    def write_call(self, function_name: str, num_args: int):
        """
        编写执行call命令的汇编代码
        """
        lines = self.build_call(function_name, num_args)
        self.lines.extend(lines)
        pass

    def build_call(self, function_name: str, num_args: int) -> list[str]:
        """
        生成函数调用代码
        参数：
        function_name(str)：函数名
        num_args(int)：函数参数
        返回值：
        list[str]：生成的代码列表
        """
        lines: list[str] = []
        fname = function_name
        if self.multi_vm and not function_name.startswith(f"{self.function_name}."):
            fname = f"{self.file_name}.{function_name}"
            pass
        self.add_comment(lines, f"// call {fname} {num_args}")
        return_address = self.create_label("RETURN_ADDRESS")
        # push return-address
        self.add_comment(lines, f"// push return_address")
        lines.append(f"@{return_address}")
        lines.append("D=A")
        lines.append("@SP")
        lines.append("A=M")
        lines.append("M=D")
        lines.append("@SP")
        lines.append("M=M+1")
        segments = ["LCL", "ARG", "THIS", "THAT"]
        for segment in segments:
            self.add_comment(lines, f"// push {segment}")
            lines.append(f"@{segment}")
            lines.append("D=M")
            lines.append("@SP")
            lines.append("A=M")
            lines.append("M=D")
            lines.append("@SP")
            lines.append("M=M+1")
        # ARG=SP-n-5
        self.add_comment(lines, f"// push ARG=SP-n-5")
        lines.append("@SP")
        lines.append("D=M")
        lines.append(f"@{num_args}")
        lines.append("D=D-A")
        lines.append(f"@5")
        lines.append("D=D-A")
        lines.append("@ARG")
        lines.append("M=D")
        # LCL=SP
        self.add_comment(lines, f"// LCL=SP")
        lines.append("@SP")
        lines.append("D=M")
        lines.append("@LCL")
        lines.append("M=D")
        # goto f
        self.add_comment(lines, f"// goto function {fname}")
        lines.append(f"@{fname}")
        lines.append("0;JMP")
        # (return-address)
        self.add_comment(lines, f"// return-address")
        lines.append(f"({return_address})")
        return lines

    def write_return(self):
        """
        编写执行return命令的汇编代码
        """
        self.add_comment(self.lines, f"// return")
        # FRAME = LCL
        self.add_comment(self.lines, f"// FRAME = LCL")
        self.lines.append("@LCL")
        self.lines.append("D=M")
        self.lines.append("@R13")
        self.lines.append("M=D")
        # RET = *(FRAME-5)
        self.add_comment(self.lines, f"// RET = *(FRAME-5)")
        self.lines.append("@5")
        self.lines.append("A=D-A")
        self.lines.append("D=M")
        self.lines.append("@R14")
        self.lines.append("M=D")
        # *ARG=pop()
        self.add_comment(self.lines, f"// *ARG=pop()")
        self.pop_to_d()
        self.lines.append("@ARG")
        self.lines.append("A=M")
        self.lines.append("M=D")
        # SP = ARG+1
        self.add_comment(self.lines, f"// SP = ARG+1")
        self.lines.append("@ARG")
        self.lines.append("D=M+1")
        self.lines.append("@SP")
        self.lines.append("M=D")
        segments = ["THAT", "THIS", "ARG", "LCL"]
        for segment in segments:
            self.add_comment(self.lines, f"// {segment}")
            self.lines.append("@R13")
            self.lines.append("D=M-1")
            self.lines.append("AM=D")
            self.lines.append("D=M")
            self.lines.append(f"@{segment}")
            self.lines.append("M=D")
        # goto RET
        self.add_comment(self.lines, f"// goto RET")
        self.lines.append("@R14")
        self.lines.append("A=M")
        self.lines.append("0;JMP")
        pass

    def write_function(self, function_name: str, num_locals: int):
        """
        编写执行function命令的汇编代码
        """
        self.function_name = function_name
        if self.multi_vm and not function_name.startswith(f"{self.file_name}."):
            self.function_name = f"{self.file_name}.{function_name}"
        if self.function_name == "Sys.init":
            self.has_init = True
        # (f)
        self.add_comment(self.lines, f"// function {self.function_name} {num_locals}")
        self.lines.append(f"({self.function_name})")
        # repeat k times:
        # PUSH 0
        self.add_comment(self.lines, f"// repeat {num_locals} times: PUSH 0")
        for i in range(num_locals):
            self.lines.append("@0")
            self.lines.append("D=A")
            self.push_from_d()
        pass

    def close(self):
        """
        关闭输出文件
        """
        if self.has_init:
            self.write_init()

        self.lines.insert(0, "@256")
        self.lines.insert(1, "D=A")
        self.lines.insert(2, "@SP")
        self.lines.insert(3, "M=D")
        self.insert_comment(self.lines, 0, "// SP=256")

        with open(self.asm_path, "w") as file_obj:
            for line in self.lines:
                file_obj.write(f"{line}\r\n")
        pass

    def add_comment(self, lines: list[str], comment: str):
        """
        添加注释
        参数：
        comment(str)：注释
        """
        if not self.output_comment:
            return
        lines.append(comment)
        pass

    def insert_comment(self, lines: list[str], index: int, comment: str):
        """
        插入注释
        参数：
        lines(list[str])：代码缓存列表
        index(int)：插入位置索引
        comment(str)：注释
        """
        if not self.output_comment:
            return
        lines.insert(index, comment)
        pass

    pass
