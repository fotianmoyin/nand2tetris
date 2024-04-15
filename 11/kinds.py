from enum import Enum


class Kinds(Enum):
    """
    变量分类
    """

    # 静态变量，全类实例共有
    STATIC = 0
    # 类变量，类实例私有
    FIELD = 1
    # 子程序参数，子程序私有
    ARG = 2
    # 子程序变量，子程序私有
    VAR = 3
    # 空分类
    NONE = 255
    pass
