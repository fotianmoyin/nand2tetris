from enum import Enum


class CommandTypes(Enum):
    """
    VM指令类型
    """

    # 算术命令
    C_ARITHMETIC = 0
    # 进栈命令
    C_PUSH = 1
    # 出栈命令
    C_POP = 2
    # 标签命令
    C_LABEL = 3
    # 跳转命令
    C_GOTO = 4
    # 判断命令
    C_IF = 5
    # 函数命令
    C_FUNCTION = 6
    # 返回命令
    C_RETURN = 7
    # 调用命令
    C_CALL = 8
    # 错误指令
    ERROR = 254
    # 注释
    COMMENT = 255
    pass
