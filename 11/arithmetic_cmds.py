from enum import Enum


class ArithmeticCmds(Enum):
    """
    算术和逻辑命令
    """

    # 整数加法
    ADD = 0
    # 整数减法
    SUB = 1
    # 算数求反
    NEG = 2
    # 相等判断
    EQ = 3
    # 大于判断
    GT = 4
    # 小于判断
    LT = 5
    # 按位“与”操作
    AND = 6
    # 按位“或”操作
    OR = 7
    # 按位“非”操作
    NOT = 8
    pass
