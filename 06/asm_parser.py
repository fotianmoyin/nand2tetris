from command_types import CommandTypes


class AsmParser:
    """
    封装对输入代码的访问操作。
    功能包括：
        读取汇编语言命令并对其进行解析；
        提供“方便访问汇编命令成分（域和符号）”的方案；
        去掉所有的空格和注释。
    """

    def __init__(self, lines: list[str]) -> None:
        """
        打开输入文件/输入流，为语法解析做准备
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
        输入当中还有更多命令吗\n
        返回：
            bool：有，返回true；否则，返回false
        """
        return len(self.lines) - self.next_line_index >= 1

    def advance(self):
        """
        从输入中读取下一条命令，将其当作“当前命令”，
        仅当has_more_commands()为真时，才能调用本程序，
        最初始的时候，没有“当前命令”
        """
        self.line = self.lines[self.next_line_index]
        self.line_index = self.next_line_index
        self.next_line_index = self.next_line_index + 1
        pass

    def command_type(self) -> CommandTypes:
        """
        返回当前命令类型\n
        返回：
            CommandTypes：当@Xxx中的Xxx是符号或十进制数字时，返回A_COMMAND；\n
            用于dest=comp;jump，返回C_COMMAND；\n
            当(Xxx)中的Xxx是符号时（实际上是伪命令），返回L_COMMAND
        """
        line = self.line
        # 去除注释
        comment_index = line.find("//")
        if comment_index > -1:
            line = line[0:comment_index]
        # 去除空格
        line = line.replace(" ", "")
        line = line.replace("\t", "")
        line = line.strip()
        if line == "":
            return CommandTypes.COMMENT

        # 命令判断
        if line.startswith("@"):
            self.cmd = line
            self.cmd_index = self.next_cmd_index
            self.next_cmd_index = self.next_cmd_index + 1
            return CommandTypes.A_COMMAND
        if line.startswith("(") and line.endswith(")"):
            self.cmd = line
            self.cmd_index = self.next_cmd_index
            self.next_cmd_index = self.next_cmd_index
            return CommandTypes.L_COMMAND
        if "=" in line or ";" in line:
            self.cmd = line
            self.cmd_index = self.next_cmd_index
            self.next_cmd_index = self.next_cmd_index + 1
            return CommandTypes.C_COMMAND
        return CommandTypes.ERROR

    def symbol(self) -> str:
        """
        返回形如@Xxx或(Xxx)的当前命令的符号或十进制值，
        仅当command_type()是A_COMMAND或L_COMMAND时才能调用\n
        返回：
            str：返回形如@Xxx或(Xxx)的当前命令的符号或十进制值
        """
        if "@" in self.cmd:
            return self.cmd[1:]
        return self.cmd[1:-1]

    def dest(self) -> str:
        """
        返回当前C指令的dest助记符（具有8种可能的形式）
        仅当command_type()是C_COMMAND时才能调用\n
        返回：
            str：dest助记符
        """
        eq_index = self.cmd.find("=")
        if eq_index > -1:
            return self.cmd[0:eq_index]
        return "Null"

    def comp(self) -> str:
        """
        返回当前C指令的comp助记符（具有28种可能的形式）
        仅当command_type()是C_COMMAND时才能调用\n
        返回：
            str：comp助记符
        """
        comp = self.cmd
        eq_index = comp.find("=")
        if eq_index > -1:
            eq_index = eq_index + 1
            comp = comp[eq_index:]
        sem_index = comp.find(";")
        if sem_index > -1:
            comp = comp[:sem_index]
        return comp

    def jump(self) -> str:
        """
        返回当前C指令的jump助记符（具有8种可能的形式）
        仅当command_type()是C_COMMAND时才能调用\n
        返回：
            str：jump助记符
        """
        sem_index = self.cmd.find(";")
        if sem_index > -1:
            sem_index = sem_index + 1
            return self.cmd[sem_index:]
        return "null"

    pass
