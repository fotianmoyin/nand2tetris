import re
from command_types import CommandTypes


class VmParser:
    """
    分析.vm文件，封装对输入代码的访问。
    它读取VM命令并解析，然后为它们的各个部分提供方便的访问入口。
    除此之外，它还能移除代码中所有的空格和注释。
    """

    def __init__(self, lines: list[str]) -> None:
        """
        打开输入文件/输入流，准备进行语法解析
        """
        self.lines = lines
        # 下一行索引
        self.next_line_index = 0
        # 下一命令索引
        self.next_cmd_index = 0
        # 当前行数据
        self.line = ""
        # 当前行索引
        self.line_index = 0
        # 当前命令
        self.cmd = ""
        # 当前命令索引
        self.cmd_index = 0
        pass

    def has_more_commands(self) -> bool:
        """
        输入当中还有更多命令吗
        返回：
        bool：有，返回true；否则，返回false
        """
        return len(self.lines) - self.next_line_index >= 1

    def advance(self):
        """
        从输入读取下一条命令，将其指定为“当前命令”，
        仅当has_more_commands()返回为真时，才能调用此程序。
        初始情况下，没有“当前命令”
        """
        self.line = self.lines[self.next_line_index]
        self.line_index = self.next_line_index
        self.next_line_index = self.next_line_index + 1
        pass

    def set_command(self, cmd):
        self.cmd = cmd
        self.cmd_index = self.next_cmd_index
        self.next_cmd_index = self.next_cmd_index + 1

    def command_type(self) -> CommandTypes:
        """
        返回当前VM命令的类型，对于所有算术命令，总是返回C_ARITHMETIC
        返回：
        CommandTypes：当前命令类型
        """
        line = self.line
        # 去除注释
        comment_index = line.find("//")
        if comment_index > -1:
            line = line[0:comment_index]
            # 去除空格
            line = line.replace("\t", " ")
        line = re.sub(" +", " ", line)
        line = line.strip()
        if line == "":
            return CommandTypes.COMMENT
        if line.startswith("push"):
            self.set_command(line)
            return CommandTypes.C_PUSH
        if line.startswith("pop"):
            self.set_command(line)
            return CommandTypes.C_POP
        if line.startswith("label"):
            self.set_command(line)
            return CommandTypes.C_LABEL
        if line.startswith("goto"):
            self.set_command(line)
            return CommandTypes.C_GOTO
        if line.startswith("if-goto"):
            self.set_command(line)
            return CommandTypes.C_IF
        if line.startswith("function"):
            self.set_command(line)
            return CommandTypes.C_FUNCTION
        if line.startswith("call"):
            self.set_command(line)
            return CommandTypes.C_CALL
        if line.startswith("return"):
            self.set_command(line)
            return CommandTypes.C_RETURN
        if (
            line.startswith("add")
            or line.startswith("sub")
            or line.startswith("neg")
            or line.startswith("eq")
            or line.startswith("gt")
            or line.startswith("lt")
            or line.startswith("and")
            or line.startswith("or")
            or line.startswith("not")
        ):
            self.set_command(line)
            return CommandTypes.C_ARITHMETIC
        return CommandTypes.ERROR

    def arg1(self) -> str:
        """
        返回当前命令的第一个参数。如果当前命令类型为C_ARITHMETIC,
        则返回命令本身（如 add,sub等）。
        当前命令类型为C_RETURN时，不应该调用本程序
        """
        args = self.cmd.split(' ')
        if len(args) == 1:
            return args[0]
        return args[1]

    def arg2(self) -> int:
        """
        返回当前命令的第二个参数。
        仅当当前命令类型为C_PUSH,C_POP,C_FUNCTION,C_CALL时，才可调用
        """
        args = self.cmd.split(' ')
        return int(args[2])

    pass
