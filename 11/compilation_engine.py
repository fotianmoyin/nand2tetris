from jack_tokenizer import JackTokenizer
from vm_writer import VMWriter
from token_types import TokenTypes
from keywords import Keywords
from symbol_table import Symbol, SymbolTable
from kinds import Kinds
from segment_types import SegmentTypes
from arithmetic_cmds import ArithmeticCmds


class CompilationEngine:
    """
    CompilationEngine:
    执行编译输出。从JackTokenizer中得到输入，
    然后将分析后的结果放入输出文件或输出流。输出是一系列compilexxx()子程序生成的，
    每个子程序对应Jack语法中的一个语法要素xxx（可以是字元或构成语句的一般符号）。
    这些程序之间约定如下：每个compilexxx()程序应该从CompilationEngine的输入中读取语法要素xxx,
    利用advance()函数取出当前要素xxx的下一个要素，并输出当前要素xxx的分析结果。
    因此，仅当下一个要素是xxx时，才会调用该要素对应的分析函数compilexxx()。
    """

    def __init__(self, tokenizer: JackTokenizer, vmwriter: VMWriter) -> None:
        """
        利用给定的输入和输出创建新的编译引擎。接下来必须调用compile_class()
        """
        self.tokenizer = tokenizer
        self.vmwriter = vmwriter
        # 类名
        self.class_name: str = None
        self.symbol_table = SymbolTable()
        # IF_TRUE 标签号
        self.if_true_index = 0
        # IF_FALSE 标签号
        self.if_false_index = 0
        # WHILE_EXP 标签号
        self.while_exp_index = 0
        # WHILE_END 标签号
        self.while_end_index = 0
        pass

    def compile_class(self):
        """
        编译整个类
        """
        # class
        keyword = self.get_keyword("关键字'class'")
        if keyword != Keywords.CLASS:
            self.raise_error("缺少关键字'class'")
        # 类名
        self.class_name = self.get_identifier("类名")
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        # 类变量声明和子过程定义
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.KEYWORD:
                keyword = self.tokenizer.keyword(token)
                if keyword == Keywords.STATIC or keyword == Keywords.FIELD:
                    # 类变量定义
                    self.compile_class_var_dec()
                    continue
                elif keyword in [
                    Keywords.CONSTRUCTOR,
                    Keywords.METHOD,
                    Keywords.FUNCTION,
                ]:
                    # 子过程定义
                    self.compile_subroutine()
                    continue
                else:
                    break
            else:
                break
        # }
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号'}'")

        # 写vm
        self.vmwriter.close()
        pass

    def compile_class_var_dec(self):
        """
        编译静态声明或字段声明
        """
        # field 或者 static
        keyword = self.get_keyword()
        kind = Kinds.NONE
        if keyword == Keywords.STATIC:
            kind = Kinds.STATIC
        if keyword == Keywords.FIELD:
            kind = Kinds.FIELD
        # 变量类型
        var_type: str = None
        token_type = self.get_token_type("变量类型")
        if token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:

                var_type = keyword.name.lower()
            else:
                self.raise_error("变量类型错误")
        elif token_type == TokenTypes.IDENTIFIER:
            var_type = self.tokenizer.identifier()
        else:
            self.raise_error("变量类型错误")
        # 变量名
        var_name = self.get_identifier("变量名称")
        self.symbol_table.define(var_name, var_type, kind)
        # 多个变量名
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type != TokenTypes.SYMBOL:
                break
            symbol = self.tokenizer.symbol(token)
            if symbol != ",":
                break
            # ,
            symbol = self.get_symbol("符号','")
            # 变量名
            var_name = self.get_identifier("变量名称")
            self.symbol_table.define(var_name, var_type, kind)
        # 分号
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        pass

    def compile_subroutine(self):
        """
        编译整个方法、函数或构造函数
        """
        # 重置子过程符号表
        self.symbol_table.start_subroutine()
        self.if_true_index = 0
        self.if_false_index = 0
        self.while_exp_index = 0
        self.while_end_index = 0
        # 函数关键字 constructor 或 method 或 function
        keyword = self.get_keyword("子过程关键字")
        is_constructor = keyword == Keywords.CONSTRUCTOR
        is_method = keyword == Keywords.METHOD
        # method方法，第一个参数为类实例
        if is_method:
            self.symbol_table.start_subroutine(1)
        # 返回类型
        token_type = self.get_token_type("返回类型")
        if token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword in [
                Keywords.VOID,
                Keywords.INT,
                Keywords.CHAR,
                Keywords.BOOLEAN,
            ]:
                pass
            else:
                self.raise_error("返回类型有误")
        elif token_type == TokenTypes.IDENTIFIER:
            identifier = self.tokenizer.identifier()
        else:
            self.raise_error("返回类型有误")
        # 函数名
        identifier = self.get_identifier("函数名")
        fun_name = f"{self.class_name}.{identifier}"
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        # 参数列表
        self.compile_parameter_list()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        # 变量声明
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type != TokenTypes.KEYWORD:
                break
            keyword = self.tokenizer.keyword(token)
            if keyword != Keywords.VAR:
                break
            self.compile_var_dec()
        self.vmwriter.write_function(fun_name, self.symbol_table.var_count(Kinds.VAR))
        if is_constructor:
            # 为类变量分配空间，设置this段
            self.vmwriter.write_push(
                SegmentTypes.CONST, self.symbol_table.var_count(Kinds.FIELD)
            )
            self.vmwriter.write_call("Memory.alloc", 1)
            self.vmwriter.write_pop(SegmentTypes.POINTER, 0)
        elif is_method:
            # 第一个参数为类实例，设置this段
            # push argument 0
            self.vmwriter.write_push(SegmentTypes.ARG, 0)
            # pop pointer 0
            self.vmwriter.write_pop(SegmentTypes.POINTER, 0)
        # 语句列表
        self.compile_statements()
        # }
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号‘}’")

        pass

    def compile_parameter_list(self):
        """
        编译参数列表（可能为空），不包含括号“（）”
        """
        while True:
            # 参数类型
            arg_type: str = None
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.KEYWORD:
                # 参数类型
                keyword = self.tokenizer.keyword(token)
                if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:
                    arg_type = self.get_keyword("参数类型")
                else:
                    break
            elif token_type == TokenTypes.IDENTIFIER:
                # 参数类型
                arg_type = self.get_identifier("参数类型")
            else:
                break
            # 参数名
            arg_name = self.get_identifier("参数名")
            self.symbol_table.define(arg_name, arg_type, Kinds.ARG)
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ",":
                # 多参数
                symbol = self.get_symbol("符号','")
            else:
                break
            pass

        pass

    def compile_var_dec(self):
        """
        编译var声明
        """
        # var
        keyword = self.get_keyword()
        # 变量类型
        var_type: str = None
        token_type = self.get_token_type("变量类型")
        if token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:
                var_type = keyword.name.lower()
            else:
                self.raise_error("变量类型错误")
        elif token_type == TokenTypes.IDENTIFIER:
            var_type = self.tokenizer.identifier()
        else:
            self.raise_error("变量类型有误")
        # 变量名
        while True:
            # 变量名
            var_name = self.get_identifier("变量名")
            self.symbol_table.define(var_name, var_type, Kinds.VAR)
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ",":
                # 多变量名
                symbol = self.get_symbol("符号','")
            else:
                break
            pass
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        pass

    def compile_statements(self):
        """
        编译一系列语句，不包含大括号“{}”
        """
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type != TokenTypes.KEYWORD:
                break
            keyword = self.tokenizer.keyword(token)
            if keyword == Keywords.LET:
                self.compile_let()
            elif keyword == Keywords.IF:
                self.compile_if()
            elif keyword == Keywords.WHILE:
                self.compile_while()
            elif keyword == Keywords.DO:
                self.compile_do()
            elif keyword == Keywords.RETURN:
                self.compile_return()
            else:
                self.raise_error("关键字错误")

        pass

    def compile_do(self):
        """
        编译do语句
        """
        # 变量名
        var_name: str = None
        # do
        keyword = self.get_keyword("do 关键字")
        # 函数名或类名或变量名
        identifier = self.get_identifier("函数名")
        # 参数数量
        arg_count = 0
        # . 或 (
        symbol = self.get_symbol("符号'('")
        if symbol == ".":
            # Xxx.yyy()
            var_name = identifier
            # 函数名
            fun_name = self.get_identifier("函数名")
            kind = self.symbol_table.kind_of(var_name)
            if kind != Kinds.NONE:
                arg_count += 1
                type = self.symbol_table.type_of(var_name)
                fun_name = f"{type}.{fun_name}"
                index = self.symbol_table.index_of(var_name)
                match kind:
                    case Kinds.STATIC:
                        self.vmwriter.write_push(SegmentTypes.STATIC, index)
                    case Kinds.FIELD:
                        self.vmwriter.write_push(SegmentTypes.THIS, index)
                    case Kinds.ARG:
                        self.vmwriter.write_push(SegmentTypes.ARG, index)
                    case Kinds.VAR:
                        self.vmwriter.write_push(SegmentTypes.LOCAL, index)
            else:
                fun_name = f"{var_name}.{fun_name}"
            # (
            symbol = self.get_symbol("符号'('")
        else:
            # yyy()
            fun_name = identifier
            self.vmwriter.write_push(SegmentTypes.POINTER, 0)
            arg_count += 1
            fun_name = f"{self.class_name}.{fun_name}"
            pass
        if symbol != "(":
            self.raise_error("缺少符号'('")
        # 表达式列表
        arg_count += self.compile_expression_list()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        # call
        self.vmwriter.write_call(fun_name, arg_count)
        self.vmwriter.write_pop(SegmentTypes.TEMP, 0)
        pass

    def compile_let(self):
        """
        编译let语句
        """
        # let
        Keyword = self.get_keyword("let 关键字")
        # 变量名
        identifier = self.get_identifier("变量名")
        var_name = identifier
        is_array = False
        # [ 或 =
        symbol = self.get_symbol("符号'='")
        if symbol == "[":
            is_array = True
            # [
            self.compile_expression()
            # ]
            symbol = self.get_symbol("符号']'")
            # push 段 0
            kind = self.symbol_table.kind_of(var_name)
            index = self.symbol_table.index_of(var_name)
            match kind:
                case Kinds.STATIC:
                    self.vmwriter.write_push(SegmentTypes.STATIC, index)
                    pass
                case Kinds.FIELD:
                    self.vmwriter.write_push(SegmentTypes.THIS, index)
                    pass
                case Kinds.ARG:
                    self.vmwriter.write_push(SegmentTypes.ARG, index)
                    pass
                case Kinds.VAR:
                    self.vmwriter.write_push(SegmentTypes.LOCAL, index)
                    pass
            # add
            self.vmwriter.write_arithmetic(ArithmeticCmds.ADD)
            # =
            symbol = self.get_symbol("符号'='")
            pass
        if symbol == "=":
            # =
            self.compile_expression()
            if is_array:
                # pop temp 0
                self.vmwriter.write_pop(SegmentTypes.TEMP, 0)
                # pop pointer 1
                self.vmwriter.write_pop(SegmentTypes.POINTER, 1)
                # push temp 0
                self.vmwriter.write_push(SegmentTypes.TEMP, 0)
                # pop that 0
                self.vmwriter.write_pop(SegmentTypes.THAT, 0)
                pass
            else:
                kind = self.symbol_table.kind_of(var_name)
                index = self.symbol_table.index_of(var_name)
                match kind:
                    case Kinds.STATIC:
                        self.vmwriter.write_pop(SegmentTypes.STATIC, index)
                        pass
                    case Kinds.FIELD:
                        self.vmwriter.write_pop(SegmentTypes.THIS, index)
                        pass
                    case Kinds.ARG:
                        self.vmwriter.write_pop(SegmentTypes.ARG, index)
                        pass
                    case Kinds.VAR:
                        self.vmwriter.write_pop(SegmentTypes.LOCAL, index)
                        pass
            pass
        else:
            self.raise_error("缺少符号'='")
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")

        pass

    def compile_while(self):
        """
        编译while语句
        """
        label_while_exp = f"WHILE_EXP{self.while_exp_index}"
        self.while_exp_index += 1
        label_while_end = f"WHILE_END{self.while_end_index}"
        self.while_end_index += 1
        # label WHILE_EXP
        self.vmwriter.write_label(label_while_exp)
        # while
        keyword = self.get_keyword("while 关键字")
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        # expression
        self.compile_expression()
        # if not goto WHILE_END
        self.vmwriter.write_arithmetic(ArithmeticCmds.NOT)
        self.vmwriter.write_if(label_while_end)
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        # statements
        self.compile_statements()
        # } 符号
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号'}'")
        # goto WHILE_EXP
        self.vmwriter.write_goto(label_while_exp)
        # label WHILE_END
        self.vmwriter.write_label(label_while_end)
        pass

    def compile_return(self):
        """
        编译return语句
        """
        # return
        keyword = self.get_keyword("return 关键字")
        # 预读取分析
        if self.tokenizer.has_more_tokens():
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ";":
                # 无返回值时，return 0
                self.vmwriter.write_push(SegmentTypes.CONST, 0)
                pass
            else:
                self.compile_expression()
                pass
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.vmwriter.write_return()
        pass

    def compile_if(self):
        """
        编译if语句，包含可选的else从句
        """
        label_if_true = f"IF_TRUE{self.if_true_index}"
        label_if_end = f"IF_END{self.if_true_index}"
        self.if_true_index += 1
        label_if_false = f"IF_FALSE{self.if_false_index}"
        self.if_false_index += 1
        # if
        keyword = self.get_keyword("if 关键字")
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        # 表达式
        self.compile_expression()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        # if goto IF_TRUE
        self.vmwriter.write_if(label_if_true)
        # goto IF_FALSE
        self.vmwriter.write_goto(label_if_false)
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        # label IF_TRUE
        self.vmwriter.write_label(label_if_true)
        # statements
        self.compile_statements()
        # }
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号'}'")
        no_else = True
        # 预读取分析
        if self.tokenizer.has_more_tokens():
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if (
                token_type == TokenTypes.KEYWORD
                and self.tokenizer.keyword(token) == Keywords.ELSE
            ):
                no_else = False
                # goto IF_END
                self.vmwriter.write_goto(label_if_end)
                # label IF_FALSE
                self.vmwriter.write_label(label_if_false)
                # else
                keyword = self.get_keyword("关键字 else")
                # {
                symbol = self.get_symbol("符号'{")
                if symbol != "{":
                    self.raise_error("缺少符号'{'")

                # statements
                self.compile_statements()
                # }
                symbol = self.get_symbol("符号'}'")
                if symbol != "}":
                    self.raise_error("缺少符号'}'")
                # label IF_END
                self.vmwriter.write_label(label_if_end)
        if no_else:
            # label IF_FALSE
            self.vmwriter.write_label(label_if_false)
        pass

    def compile_expression(self):
        """
        编译一个表达式
        """
        # term
        self.compile_term()
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type != TokenTypes.SYMBOL:
                break
            symbol = self.tokenizer.symbol(token)
            if symbol not in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                break
            # 二元操作符
            symbol = self.get_symbol()
            # term
            self.compile_term()
            # 算术逻辑操作
            match symbol:
                case "+":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.ADD)
                case "-":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.SUB)
                case "*":
                    self.vmwriter.write_call("Math.multiply", 2)
                case "/":
                    self.vmwriter.write_call("Math.divide", 2)
                case "&":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.AND)
                case "|":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.OR)
                case "<":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.LT)
                case ">":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.GT)
                case "=":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.EQ)

        pass

    def compile_term(self):
        """
        编译一个“term”。本程序在“从多种可能的分析规则中作出决策”的时候会遇到一点难度。
        特别是，如果当前字元为标识符，那么本程序就须要区分变量、数组、子程序调用这三种情况。
        通过提前查看下一个字元（可以为“[”、”(“或”.“），就可以区分这三种可能性了。
        后续任何其他字元都不属于这个term,故不须要取用
        """
        token_type = self.get_token_type("表达式")
        if token_type == TokenTypes.INT_CONST:
            int_val = self.tokenizer.int_val()
            # push constant int_val
            self.vmwriter.write_push(SegmentTypes.CONST, int_val)
        elif token_type == TokenTypes.STRING_CONST:
            string_val = self.tokenizer.string_val()
            # push constant 字符串长度
            self.vmwriter.write_push(SegmentTypes.CONST, len(string_val))
            # call String.new 1
            self.vmwriter.write_call("String.new", 1)
            # 将字符串一个字符一个字符的追加到字符串数组
            for s in string_val:
                # push constant 字符值
                self.vmwriter.write_push(SegmentTypes.CONST, ord(s))
                # call String.appendChar 2
                self.vmwriter.write_call("String.appendChar", 2)
        elif token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword not in [
                Keywords.TRUE,
                Keywords.FALSE,
                Keywords.NULL,
                Keywords.THIS,
            ]:
                self.raise_error("表达式有误")
            if keyword == Keywords.TRUE:
                # self.vmwriter.write_push(SegmentTypes.CONST, 1)
                # self.vmwriter.write_arithmetic(ArithmeticCmds.NEG)
                self.vmwriter.write_push(SegmentTypes.CONST, 0)
                self.vmwriter.write_arithmetic(ArithmeticCmds.NOT)
                pass
            elif keyword == Keywords.FALSE:
                self.vmwriter.write_push(SegmentTypes.CONST, 0)
                pass
            elif keyword == Keywords.NULL:
                self.vmwriter.write_push(SegmentTypes.CONST, 0)
                pass
            elif keyword == Keywords.THIS:
                self.vmwriter.write_push(SegmentTypes.POINTER, 0)
                pass
        elif token_type == TokenTypes.SYMBOL:
            symbol = self.tokenizer.symbol()
            if symbol == "(":
                self.compile_expression()
                symbol = self.get_symbol("符号')'")
                if symbol != ")":
                    self.raise_error("缺少符号')'")
            elif symbol in ["-", "~"]:
                self.compile_term()
                if symbol == "-":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.NEG)
                elif symbol == "~":
                    self.vmwriter.write_arithmetic(ArithmeticCmds.NOT)
            else:
                self.raise_error("符号错误")
            pass
        elif token_type == TokenTypes.IDENTIFIER:
            # 数组、子过程或单变量
            var_name = self.tokenizer.identifier()
            only_var = True
            # 预读取分析
            if self.tokenizer.has_more_tokens():
                token = self.tokenizer.inadvance()
                token_type = self.tokenizer.token_type(token)
                if token_type == TokenTypes.SYMBOL:
                    symbol = self.tokenizer.symbol(token)
                    if symbol == "[":
                        # 数组
                        only_var = False
                        # [
                        symbol = self.get_symbol()
                        # 表达式
                        self.compile_expression()
                        # ]
                        symbol = self.get_symbol()
                        if symbol != "]":
                            self.raise_error("缺少符号']'")
                        # 数组操作
                        kind = self.symbol_table.kind_of(var_name)
                        type = self.symbol_table.type_of(var_name)
                        index = self.symbol_table.index_of(var_name)
                        match kind:
                            case Kinds.STATIC:
                                self.vmwriter.write_push(SegmentTypes.STATIC, index)
                                pass
                            case Kinds.FIELD:
                                self.vmwriter.write_push(SegmentTypes.THIS, index)
                                pass
                            case Kinds.ARG:
                                self.vmwriter.write_push(SegmentTypes.ARG, index)
                                pass
                            case Kinds.VAR:
                                self.vmwriter.write_push(SegmentTypes.LOCAL, index)
                                pass
                        self.vmwriter.write_arithmetic(ArithmeticCmds.ADD)
                        self.vmwriter.write_pop(SegmentTypes.POINTER, 1)
                        self.vmwriter.write_push(SegmentTypes.THAT, 0)
                        pass
                    elif symbol in ["(", "."]:
                        # 子过程
                        only_var = False
                        arg_count = 0
                        # . 或 (
                        symbol = self.get_symbol("符号'('")
                        if symbol == ".":
                            # Xxx.yyy()
                            # 函数名
                            fun_name = self.get_identifier("函数名")
                            kind = self.symbol_table.kind_of(var_name)
                            if kind != Kinds.NONE:
                                arg_count += 1
                                type = self.symbol_table.type_of(var_name)
                                fun_name = f"{type}.{fun_name}"
                                index = self.symbol_table.index_of(var_name)
                                match kind:
                                    case Kinds.STATIC:
                                        self.vmwriter.write_push(
                                            SegmentTypes.STATIC, index
                                        )
                                    case Kinds.FIELD:
                                        self.vmwriter.write_push(
                                            SegmentTypes.THIS, index
                                        )
                                    case Kinds.ARG:
                                        self.vmwriter.write_push(
                                            SegmentTypes.ARG, index
                                        )
                                    case Kinds.VAR:
                                        self.vmwriter.write_push(
                                            SegmentTypes.LOCAL, index
                                        )
                            else:
                                fun_name = f"{var_name}.{fun_name}"
                            # (
                            symbol = self.get_symbol("符号'('")
                        else:
                            # yyy()
                            fun_name = var_name
                            self.vmwriter.write_push(SegmentTypes.POINTER, 0)
                            arg_count += 1;
                            fun_name = f"{self.class_name}.{fun_name}"
                            pass
                        # (
                        if symbol != "(":
                            self.raise_error("缺少符号'('")
                        # 表达式列表
                        arg_count += self.compile_expression_list()
                        # )
                        symbol = self.get_symbol("符号')'")
                        if symbol != ")":
                            self.raise_error("缺少符号')'")
                        # call
                        self.vmwriter.write_call(fun_name, arg_count)
                        pass
                    pass
                pass
            # 完成预读分析后
            if only_var:
                kind = self.symbol_table.kind_of(var_name)
                index = self.symbol_table.index_of(var_name)
                match kind:
                    case Kinds.STATIC:
                        self.vmwriter.write_push(SegmentTypes.STATIC, index)
                        pass
                    case Kinds.FIELD:
                        self.vmwriter.write_push(SegmentTypes.THIS, index)
                        pass
                    case Kinds.ARG:
                        self.vmwriter.write_push(SegmentTypes.ARG, index)
                        pass
                    case Kinds.VAR:
                        self.vmwriter.write_push(SegmentTypes.LOCAL, index)
                        pass

        pass

    def compile_expression_list(self) -> int:
        """
        编译由逗号分隔的表达式列表（可能为空）
        返回值：
        int:参数个数
        """
        arg_count = 0
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) not in [
                "(",
                "-",
                "~",
            ]:
                break
            # 表达式
            self.compile_expression()
            arg_count += 1
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type != TokenTypes.SYMBOL:
                break
            symbol = self.tokenizer.symbol(token)
            if symbol != ",":
                break
            # ,
            symbol = self.get_symbol()

        return arg_count

    def get_keyword(self, comment: str = None) -> Keywords:
        """
        读取关键字
        """
        token_type = self.get_token_type()
        if token_type != TokenTypes.KEYWORD:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.keyword()

    def get_symbol(self, comment: str = None) -> str:
        """
        读取符号
        """
        token_type = self.get_token_type(comment)
        if token_type != TokenTypes.SYMBOL:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.symbol()

    def get_identifier(self, comment: str = None) -> str:
        """
        读取标识符
        """
        token_type = self.get_token_type(comment)
        if token_type != TokenTypes.IDENTIFIER:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.identifier()

    def get_token_type(self, comment: str = None) -> TokenTypes:
        """
        读取字元类型
        """
        if not self.tokenizer.has_more_tokens():
            self.raise_error(f"缺少{comment}")
        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        return token_type

    def raise_error(self, err: str, line_num: int = -1):
        """
        抛出错误
        """
        pre = ""
        if line_num == -1:
            if self.tokenizer.token != None:
                line_num = self.tokenizer.token.line + 1
                pre = f"{self.tokenizer.token.txt} 附近"
            else:
                line_num = 1
        raise ValueError(f"在 {self.tokenizer.jack_name} （行 {line_num}）：{pre}，{err}")

    pass
