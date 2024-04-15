from enum import Enum


class TokenTypes(Enum):
    """
    字元类型
    """

    # 关键字
    KEYWORD = 0
    # 符号
    SYMBOL = 1
    # 标识符
    IDENTIFIER = 2
    # 数值常量
    INT_CONST = 3
    # 字符串常量
    STRING_CONST = 4
    pass
