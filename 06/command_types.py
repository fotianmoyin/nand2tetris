from enum import Enum


class CommandTypes(Enum):
    """
    汇编指令类型
    """
    # A指令
    A_COMMAND = 0
    # C指令
    C_COMMAND = 1
    # 伪指令
    L_COMMAND = 2
    # 错误指令
    ERROR = 254
    # 注释
    COMMENT = 255
    pass
