from segment_types import SegmentTypes
from arithmetic_cmds import ArithmeticCmds


class VMWriter:
    """
    使用VM命令语法，将VM命令写入文件
    """

    def __init__(self, vm_path: str) -> None:
        """
        创建新的待写文件
        参数：
        vm_path(str):vm文件路径
        """
        self.vm_path = vm_path
        self.lines: list[str] = []
        pass

    def write_push(self, segment: SegmentTypes, index: int):
        """
        写入VM push命令
        参数：
        index(int):区段索引
        """
        match segment:
            case SegmentTypes.CONST:
                self.lines.append(f"push constant {index}")
                pass
            case SegmentTypes.ARG:
                self.lines.append(f"push argument {index}")
                pass
            case SegmentTypes.LOCAL:
                self.lines.append(f"push local {index}")
                pass
            case SegmentTypes.STATIC:
                self.lines.append(f"push static {index}")
                pass
            case SegmentTypes.THIS:
                self.lines.append(f"push this {index}")
                pass
            case SegmentTypes.THAT:
                self.lines.append(f"push that {index}")
                pass
            case SegmentTypes.POINTER:
                self.lines.append(f"push pointer {index}")
                pass
            case SegmentTypes.TEMP:
                self.lines.append(f"push temp {index}")
                pass
        pass

    def write_pop(self, segment: SegmentTypes, index: int):
        """
        写入VM pop命令
        参数：
        index(int):区段索引
        """
        match segment:
            case SegmentTypes.CONST:
                self.lines.append(f"pop constant {index}")
                pass
            case SegmentTypes.ARG:
                self.lines.append(f"pop argument {index}")
                pass
            case SegmentTypes.LOCAL:
                self.lines.append(f"pop local {index}")
                pass
            case SegmentTypes.STATIC:
                self.lines.append(f"pop static {index}")
                pass
            case SegmentTypes.THIS:
                self.lines.append(f"pop this {index}")
                pass
            case SegmentTypes.THAT:
                self.lines.append(f"pop that {index}")
                pass
            case SegmentTypes.POINTER:
                self.lines.append(f"pop pointer {index}")
                pass
            case SegmentTypes.TEMP:
                self.lines.append(f"pop temp {index}")
                pass
        pass

    def write_arithmetic(self, command: ArithmeticCmds):
        """
        写入VM 算术命令
        参数：
        command(ArithmeticCmds):算术命令
        """
        match command:
            case ArithmeticCmds.ADD:
                self.lines.append("add")
                pass
            case ArithmeticCmds.SUB:
                self.lines.append("sub")
                pass
            case ArithmeticCmds.NEG:
                self.lines.append("neg")
                pass
            case ArithmeticCmds.EQ:
                self.lines.append("eq")
                pass
            case ArithmeticCmds.GT:
                self.lines.append("gt")
                pass
            case ArithmeticCmds.LT:
                self.lines.append("lt")
                pass
            case ArithmeticCmds.AND:
                self.lines.append("and")
                pass
            case ArithmeticCmds.OR:
                self.lines.append("or")
                pass
            case ArithmeticCmds.NOT:
                self.lines.append("not")
                pass
        pass

    def write_label(self, label: str):
        """
        写入VM label命令
        参数：
        label(str):标签名
        """
        self.lines.append(f"label {label}")
        pass

    def write_goto(self, label: str):
        """
        写入VM goto命令
        参数：
        label(str):标签名
        """
        self.lines.append(f"goto {label}")
        pass

    def write_if(self, label: str):
        """
        写入VM if-goto命令
        参数：
        label(str):标签名
        """
        self.lines.append(f"if-goto {label}")
        pass

    def write_call(self, name: str, n_args: int):
        """
        写入VM call命令
        参数：
        name(str):函数名
        n_args(int):参数个数
        """
        self.lines.append(f"call {name} {n_args}")
        pass

    def write_function(self, name: str, n_args: int):
        """
        写入VM function命令
        参数：
        name(str):函数名
        n_args(int):变量个数
        """
        self.lines.append(f"function {name} {n_args}")
        pass

    def write_return(self):
        """
        写入VM return命令
        """
        self.lines.append("return")
        pass

    def close(self):
        """
        关闭输出文件
        """
        with open(self.vm_path, "w") as file_obj:
            for line in self.lines:
                file_obj.write(f"{line}\r\n")
        pass

    pass
