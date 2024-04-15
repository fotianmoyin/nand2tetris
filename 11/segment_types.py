from enum import Enum


class SegmentTypes(Enum):
    """
    区段类型
    """
    CONST=0
    ARG=1
    LOCAL=2
    STATIC=3
    THIS=4
    THAT=5
    POINTER=6
    TEMP=7
    pass