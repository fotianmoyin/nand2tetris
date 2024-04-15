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
        self.lines: list[str] = []
        self.lines.append('@256')
        self.lines.append('D=A')
        self.lines.append('@SP')
        self.lines.append('M=D')
        self.sys_labels: dict[str, bool] = {}
        pass

    def set_file_name(self, file_name: str):
        """
        通知代码写入程序，新的VM文件翻译过程已经开始
        参数：
        file_name(str)：vm文件名
        """
        self.file_name = file_name
        pass

    def write_arithmetic(self, command: str):
        """
        将给定的算术操作所对应的汇编代码写至输出
        参数：
        command(str)：命令
        """
        match command:
            case "add":
                # 整数加法
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=M+D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "sub":
                # 整数减法
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=M-D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "neg":
                # 算数求反
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=-M")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "eq":
                # 相等判断
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("D=M-D")
                eq_label = self.create_label('EQ')
                self.lines.append(f"@{eq_label}")
                self.lines.append("D;JEQ")
                self.lines.append("D=0")
                output_label = self.create_label('OUTPUT')
                self.lines.append(f"@{output_label}")
                self.lines.append("0;JMP")
                self.lines.append(f"({eq_label})")
                self.lines.append("D=-1")
                self.lines.append(f"({output_label})")
                self.lines.append("@SP")
                self.lines.append("A=M")
                self.lines.append("M=D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "gt":
                # 大于判断
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("D=M-D")
                gt_label = self.create_label('GT')
                self.lines.append(f"@{gt_label}")
                self.lines.append("D;JGT")
                self.lines.append("D=0")
                output_label = self.create_label('OUTPUT')
                self.lines.append(f"@{output_label}")
                self.lines.append("0;JMP")
                self.lines.append(f"({gt_label})")
                self.lines.append("D=-1")
                self.lines.append(f"({output_label})")
                self.lines.append("@SP")
                self.lines.append("A=M")
                self.lines.append("M=D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "lt":
                # 小于判断
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("D=M-D")
                lt_label = self.create_label('LT')
                self.lines.append(f"@{lt_label}")
                self.lines.append("D;JLT")
                self.lines.append("D=0")
                output_label = self.create_label('OUTPUT')
                self.lines.append(f"@{output_label}")
                self.lines.append("0;JMP")
                self.lines.append(f"({lt_label})")
                self.lines.append("D=-1")
                self.lines.append(f"({output_label})")
                self.lines.append("@SP")
                self.lines.append("A=M")
                self.lines.append("M=D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "and":
                # 按位“与”操作
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=M&D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "or":
                # 按位“或”操作
                self.pop_to_d()
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=M|D")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
            case "not":
                # 按位“非”操作
                self.lines.append("@SP")
                self.lines.append("M=M-1")
                self.lines.append("A=M")
                self.lines.append("M=!M")
                self.lines.append("@SP")
                self.lines.append("M=M+1")
                pass
        pass

    def create_label(self, prefix:str) -> str:
        for i in range(1000):
            label = "".join(random.sample(string.ascii_uppercase, 5))
            if label not in self.sys_labels.keys():
                self.sys_labels[label] = True
                return f"{self.file_name}.{prefix}.{label}"
        return None

    def write_push_pop(self, command_type: CommandTypes, segment: str, index: int):
        """
        将给定的command（命令类型为C_PUSH或C_POP）所对应的汇编代码写入至输出
        参数：
        command_type(CommandTypes)：命令类型
        segment(str)：内存段
        index(int)：内存段中内存单元索引
        """
        if command_type == CommandTypes.C_PUSH:
            match segment:
                case "argument":
                    # 存储函数的参数
                    self.lines.append("@ARG")
                    self.lines.append("D=M")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("A=D")
                    self.lines.append("D=M")
                    pass
                case "local":
                    # 存储函数的局部变量
                    self.lines.append("@LCL")
                    self.lines.append("D=M")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("A=D")
                    self.lines.append("D=M")
                    pass
                case "static":
                    # 存储同一.vm文件中所有函数共享的静态变量
                    self.lines.append(f"@{self.file_name}.{index}")
                    self.lines.append("D=M")
                    pass
                case "constant":
                    # 包含所有常数的伪段，常数的范围为0...32767
                    self.lines.append(f"@{index}")
                    self.lines.append("D=A")
                    pass
                case "this":
                    # 通用段，能够与堆中不同区域相对应来满足各种程序编写需求
                    self.lines.append("@THIS")
                    self.lines.append("D=M")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("A=D")
                    self.lines.append("D=M")
                    pass
                case "that":
                    # 能够与堆中不同区域相对应来满足各种程序编写需求
                    self.lines.append("@THAT")
                    self.lines.append("D=M")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("A=D")
                    self.lines.append("D=M")
                    pass
                case "pointer":
                    # 该段由2个内存单元组成，用来保存this和that段的基地址，
                    # 任何VM函数可以将pointer0（或1）设置到某一地址上，
                    # 这相当于将this（或that）段联结到起始于该地址的堆区域上
                    if index == 0:
                        self.lines.append("@THIS")
                    if index == 1:
                        self.lines.append("@THAT")
                    self.lines.append("D=M")
                    pass
                case "temp":
                    # 固定的段，由8个内存单元组成，用来保存临时变量
                    self.lines.append("@R5")
                    self.lines.append("D=A")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("A=D")
                    self.lines.append("D=M")
                    pass
            self.lines.append("@SP")
            self.lines.append("A=M")
            self.lines.append("M=D")
            self.lines.append("@SP")
            self.lines.append("M=M+1")
            pass

        if command_type == CommandTypes.C_POP:
            match segment:
                case "argument":
                    # 存储函数的参数
                    self.lines.append("@ARG")
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
                case "local":
                    # 存储函数的局部变量
                    self.lines.append("@LCL")
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
                case "static":
                    # 存储同一.vm文件中所有函数共享的静态变量
                    self.pop_to_d()
                    self.lines.append(f"@{self.file_name}.{index}")
                    self.lines.append("M=D")
                    pass
                case "constant":
                    # 包含所有常数的伪段，常数的范围为0...32767
                    pass
                case "this":
                    # 通用段，能够与堆中不同区域相对应来满足各种程序编写需求
                    self.lines.append("@THIS")
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
                case "that":
                    # 能够与堆中不同区域相对应来满足各种程序编写需求
                    self.lines.append("@THAT")
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
                case "pointer":
                    # 该段由2个内存单元组成，用来保存this和that段的基地址，
                    # 任何VM函数可以将pointer0（或1）设置到某一地址上，
                    # 这相当于将this（或that）段联结到起始于该地址的堆区域上
                    self.pop_to_d()
                    if index == 0:
                        self.lines.append("@THIS")
                    if index == 1:
                        self.lines.append("@THAT")
                    self.lines.append("M=D")
                    pass
                case "temp":
                    # 固定的段，由8个内存单元组成，用来保存临时变量
                    self.lines.append(f"@R5")
                    self.lines.append("D=A")
                    self.lines.append(f"@{index}")
                    self.lines.append("D=D+A")
                    self.lines.append("@R13")
                    self.lines.append("M=D")
                    self.pop_to_d()
                    self.lines.append("@R13")
                    self.lines.append("A=M")
                    self.lines.append("M=D")
                    pass

            pass
        pass

    def pop_to_d(self):
        self.lines.append("@SP")
        self.lines.append("M=M-1")
        self.lines.append("A=M")
        self.lines.append("D=M")
        pass

    def close(self):
        """
        关闭输出文件
        """
        with open(self.asm_path, "w") as file_obj:
            for line in self.lines:
                file_obj.write(f'{line}\r\n')
        pass

    pass
