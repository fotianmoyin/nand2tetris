from kinds import Kinds


class Symbol:
    """
    符号
    """

    def __init__(self, type: str, kind: Kinds, index: int) -> None:
        self.type = type
        self.kind = kind
        self.index = index
        pass

    pass


class SymbolTable:
    """
    符号表
    该模块提供创建和使用符号表的服务。每个符号都具有作用域，符号只有在源代码中的这个作用域内才是可见的。
    符号表通过为每个在作用域里的符号赋予一个动态变化的数值来实现。索引从0开始，每当一个标识符被添加，
    就自增1,当开始新作用域时，索引就被重置为0。
    """

    def __init__(self) -> None:
        """
        创建新的空符号表
        """
        self.class_table: dict[str, Symbol] = {}
        self.static_index = 0
        self.field_index = 0
        self.sub_table: dict[str, Symbol] = {}
        self.arg_index = 0
        self.var_index = 0
        pass

    def start_subroutine(self, arg_index = 0):
        """
        开创新的子程序作用域（即将子程序的符号表重置）
        """
        self.sub_table.clear()
        self.arg_index = arg_index
        self.var_index = 0
        pass

    def define(self, name: str, type: str, kind: Kinds):
        """
        定义给定了名称、类型和分类的新标识符，并赋给它一个索引。
        STATIC和FIELD标识符的作用域是整个类，ARG和VAR的作用域是整个子程序
        参数：
        name(str):变量名称
        type(str):变量类型
        kind(VariableKinds):变量分类
        """
        match kind:
            case Kinds.STATIC:
                if name not in self.class_table.keys():
                    self.class_table[name] = Symbol(type, kind, self.static_index)
                    self.static_index = self.static_index + 1
                pass
            case Kinds.FIELD:
                if name not in self.class_table.keys():
                    self.class_table[name] = Symbol(type, kind, self.field_index)
                    self.field_index = self.field_index + 1
                pass
            case Kinds.ARG:
                if name not in self.sub_table.keys():
                    self.sub_table[name] = Symbol(type, kind, self.arg_index)
                    self.arg_index = self.arg_index + 1
                pass
            case Kinds.VAR:
                if name not in self.sub_table.keys():
                    self.sub_table[name] = Symbol(type, kind, self.var_index)
                    self.var_index = self.var_index + 1
                pass
        pass

    def var_count(self, kind: Kinds) -> int:
        """
        返回已经定义在当前作用域内的变量的数量
        参数：
        kind(VariableKinds):变量分类
        """
        match kind:
            case Kinds.STATIC:
                return self.static_index
            case Kinds.FIELD:
                return self.field_index
            case Kinds.ARG:
                return self.arg_index
            case Kinds.VAR:
                return self.var_index
        return 0

    def kind_of(self, name: str) -> Kinds:
        """
        返回当前作用域内的标识符的种类。如果该标识符在当前作用域内是未知的，那么返回NONE
        参数：
        name(str):变量名称
        """
        if name in self.sub_table.keys():
            symbol = self.sub_table[name]
            return symbol.kind
        elif name in self.class_table.keys():
            symbol = self.class_table[name]
            return symbol.kind
        else:
            return Kinds.NONE

    def type_of(self, name: str) -> str:
        """
        返回当前作用域内标识符的类型
        参数：
        name(str):变量名称
        返回值：
        str:变量类型
        """
        if name in self.sub_table.keys():
            symbol = self.sub_table[name]
            return symbol.type
        elif name in self.class_table.keys():
            symbol = self.class_table[name]
            return symbol.type
        else:
            return None

    def index_of(self, name: str) -> int:
        """
        返回标识符的索引
        参数：
        name(str):变量名称
        返回值：
        int:标识符的索引
        """
        if name in self.sub_table.keys():
            symbol = self.sub_table[name]
            return symbol.index
        elif name in self.class_table.keys():
            symbol = self.class_table[name]
            return symbol.index
        else:
            return -1

    pass
