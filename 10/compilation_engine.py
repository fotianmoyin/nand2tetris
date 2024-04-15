from jack_tokenizer import JackTokenizer
from token_types import TokenTypes
from keywords import Keywords


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

    def __init__(self, tokenizer: JackTokenizer, xml_path: str) -> None:
        """
        利用给定的输入和输出创建新的编译引擎。接下来必须调用compile_class()
        """
        self.tokenizer = tokenizer
        self.xml_path = xml_path
        self.lines: list[str] = []
        pass

    def compile_class(self):
        """
        编译整个类
        """
        # 类标签
        tag = "class"
        self.write_opening_tag(tag)
        # class
        keyword = self.get_keyword("关键字'class'")
        if keyword != Keywords.CLASS:
            self.raise_error("缺少关键字'class'")
        self.write_keyword(keyword)
        # 类名
        identifier = self.get_identifier("类名")
        self.write_identifier(identifier)
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        self.write_symbol(symbol)

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
                    # 子函数定义
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
        self.write_symbol(symbol)
        # 类标签
        self.write_closing_tag(tag)
        # 写xml
        self.write_xml()
        pass

    def compile_class_var_dec(self):
        """
        编译静态声明或字段声明
        """
        tag = "classVarDec"
        self.write_opening_tag(tag)
        # field 或者 static
        keyword = self.get_keyword()
        self.write_keyword(keyword)
        # 变量类型
        token_type = self.get_token_type("变量类型")
        if token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:
                self.write_keyword(keyword)
            else:
                self.raise_error("变量类型错误")
        elif token_type == TokenTypes.IDENTIFIER:
            identifier = self.tokenizer.identifier()
            self.write_identifier(identifier)
        else:
            self.raise_error("变量类型错误")
        # 变量名
        identifier = self.get_identifier("变量名称")
        self.write_identifier(identifier)
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
            # 多个变量名
            symbol = self.get_symbol("符号','")
            self.write_symbol(symbol)
            identifier = self.get_identifier("变量名称")
            self.write_identifier(identifier)
        # 分号
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.write_symbol(symbol)
        # 类变量定义标签
        self.write_closing_tag(tag)
        pass

    def compile_subroutine(self):
        """
        编译整个方法、函数或构造函数
        """
        # 子过程标签
        tag = "subroutineDec"
        self.write_opening_tag(tag)
        # 函数关键字 constructor 或 method 或 function
        keyword = self.get_keyword("子过程关键字")
        self.write_keyword(keyword)
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
                self.write_keyword(keyword)
            else:
                self.raise_error("返回类型有误")
        elif token_type == TokenTypes.IDENTIFIER:
            identifier = self.tokenizer.identifier()
            self.write_identifier(identifier)
        else:
            self.raise_error("返回类型有误")
        # 函数名
        identifier = self.get_identifier("函数名")
        self.write_identifier(identifier)
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        self.write_symbol(symbol)
        # 参数列表
        self.compile_parameter_list()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        self.write_symbol(symbol)
        # 函数体开始
        body_tag = "subroutineBody"
        self.write_opening_tag(body_tag)
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        self.write_symbol(symbol)

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
        # 语句列表
        self.compile_statements()
        # }
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号‘}’")
        self.write_symbol(symbol)
        # 函数体标签
        self.write_closing_tag(body_tag)
        # 函数标签
        self.write_closing_tag(tag)
        pass

    def compile_parameter_list(self):
        """
        编译参数列表（可能为空），不包含括号“（）”
        """
        # 参数标签
        tag = "parameterList"
        self.write_opening_tag(tag)
        while True:
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.KEYWORD:
                # 参数类型
                keyword = self.tokenizer.keyword(token)
                if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:
                    keyword = self.get_keyword("参数类型")
                    self.write_keyword(keyword)
                else:
                    break
            elif token_type == TokenTypes.IDENTIFIER:
                # 参数类型
                identifier = self.get_identifier("参数类型")
                self.write_identifier(identifier)
            else:
                break
            # 参数名
            identifier = self.get_identifier("参数名")
            self.write_identifier(identifier)
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ",":
                # 多参数
                symbol = self.get_symbol("符号','")
                self.write_symbol(symbol)
            else:
                break
            pass
        self.write_closing_tag(tag)
        pass

    def compile_var_dec(self):
        """
        编译var声明
        """
        # 变量声明标签
        tag = "varDec"
        self.write_opening_tag(tag)
        # var
        keyword = self.get_keyword()
        self.write_keyword(keyword)
        # 变量类型
        token_type = self.get_token_type("变量类型")
        if token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword in [Keywords.INT, Keywords.CHAR, Keywords.BOOLEAN]:
                self.write_keyword(keyword)
            else:
                self.raise_error("变量类型错误")
        elif token_type == TokenTypes.IDENTIFIER:
            identifier = self.tokenizer.identifier()
            self.write_identifier(identifier)
        else:
            self.raise_error("变量类型有误")
        # 变量名
        while True:
            # 变量名
            identifier = self.get_identifier("变量名")
            self.write_identifier(identifier)
            # 预读取分析
            if not self.tokenizer.has_more_tokens():
                break
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ",":
                # 多变量名
                symbol = self.get_symbol("符号','")
                self.write_symbol(symbol)
            else:
                break
            pass
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.write_symbol(symbol)
        # 变量声明标签
        self.write_closing_tag(tag)
        pass

    def compile_statements(self):
        """
        编译一系列语句，不包含大括号“{}”
        """
        # 语句标签
        tag = "statements"
        self.write_opening_tag(tag)
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

        self.write_closing_tag(tag)
        pass

    def compile_do(self):
        """
        编译do语句
        """
        tag = "doStatement"
        self.write_opening_tag(tag)
        # do
        keyword = self.get_keyword("do 关键字")
        self.write_keyword(keyword)
        # 函数名或类名或变量名
        identifier = self.get_identifier("函数名")
        self.write_identifier(identifier)
        # . 或 (
        symbol = self.get_symbol("符号'('")
        if symbol == ".":
            self.write_symbol(symbol)
            # 函数名
            identifier = self.get_identifier("函数名")
            self.write_identifier(identifier)
            # (
            symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        self.write_symbol(symbol)
        # 表达式列表
        self.compile_expression_list()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        self.write_symbol(symbol)
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def compile_let(self):
        """
        编译let语句
        """
        # let语句
        tag = "letStatement"
        self.write_opening_tag(tag)
        # let
        Keyword = self.get_keyword("let 关键字")
        self.write_keyword(Keyword)
        # 变量名
        identifier = self.get_identifier("变量名")
        self.write_identifier(identifier)
        # [ 或 =
        symbol = self.get_symbol("符号'='")
        if symbol == "[":
            # [
            self.write_symbol(symbol)
            self.compile_expression()
            # ]
            symbol = self.get_symbol("符号']'")
            self.write_symbol(symbol)
            symbol = self.get_symbol("符号'='")
            pass
        if symbol == "=":
            # =
            self.write_symbol(symbol)
            self.compile_expression()
            pass
        else:
            self.raise_error("缺少符号'='")
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.write_symbol(symbol)
        self.write_closing_tag(tag)

        pass

    def compile_while(self):
        """
        编译while语句
        """
        tag = "whileStatement"
        self.write_opening_tag(tag)
        # while
        keyword = self.get_keyword("while 关键字")
        self.write_keyword(keyword)
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        self.write_symbol(symbol)
        # expression
        self.compile_expression()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        self.write_symbol(symbol)
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        self.write_symbol(symbol)
        # statements
        self.compile_statements()
        # } 符号
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号'}'")
        self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def compile_return(self):
        """
        编译return语句
        """
        tag = "returnStatement"
        self.write_opening_tag(tag)
        # return
        keyword = self.get_keyword("return 关键字")
        self.write_keyword(keyword)
        # 预读取分析
        if self.tokenizer.has_more_tokens():
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if token_type == TokenTypes.SYMBOL and self.tokenizer.symbol(token) == ";":
                pass
            else:
                self.compile_expression()
                pass
        # ;
        symbol = self.get_symbol("符号';'")
        if symbol != ";":
            self.raise_error("缺少符号';'")
        self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def compile_if(self):
        """
        编译if语句，包含可选的else从句
        """
        tag = "ifStatement"
        self.write_opening_tag(tag)
        # if
        keyword = self.get_keyword("if 关键字")
        self.write_keyword(keyword)
        # (
        symbol = self.get_symbol("符号'('")
        if symbol != "(":
            self.raise_error("缺少符号'('")
        self.write_symbol(symbol)
        # 表达式
        self.compile_expression()
        # )
        symbol = self.get_symbol("符号')'")
        if symbol != ")":
            self.raise_error("缺少符号')'")
        self.write_symbol(symbol)
        # {
        symbol = self.get_symbol("符号'{'")
        if symbol != "{":
            self.raise_error("缺少符号'{'")
        self.write_symbol(symbol)
        # statements
        self.compile_statements()
        # }
        symbol = self.get_symbol("符号'}'")
        if symbol != "}":
            self.raise_error("缺少符号'}'")
        self.write_symbol(symbol)
        # 预读取分析
        if self.tokenizer.has_more_tokens():
            token = self.tokenizer.inadvance()
            token_type = self.tokenizer.token_type(token)
            if (
                token_type == TokenTypes.KEYWORD
                and self.tokenizer.keyword(token) == Keywords.ELSE
            ):
                # else
                keyword = self.get_keyword("关键字 else")
                self.write_keyword(keyword)
                # {
                symbol = self.get_symbol("符号'{")
                if symbol != "{":
                    self.raise_error("缺少符号'{'")
                self.write_symbol(symbol)
                # statements
                self.compile_statements()
                # }
                symbol = self.get_symbol("符号'}'")
                if symbol != "}":
                    self.raise_error("缺少符号'}'")
                self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def compile_expression(self):
        """
        编译一个表达式
        """
        tag = "expression"
        self.write_opening_tag(tag)
        while True:
            self.compile_term()
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
            self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def compile_term(self):
        """
        编译一个“term”。本程序在“从多种可能的分析规则中作出决策”的时候会遇到一点难度。
        特别是，如果当前字元为标识符，那么本程序就须要区分变量、数组、子程序调用这三种情况。
        通过提前查看下一个字元（可以为“[”、”(“或”.“），就可以区分这三种可能性了。
        后续任何其他字元都不属于这个term,故不须要取用
        """
        tag = "term"
        self.write_opening_tag(tag)
        token_type = self.get_token_type("表达式")
        if token_type == TokenTypes.INT_CONST:
            int_val = self.tokenizer.int_val()
            self.write_int(int_val)
        elif token_type == TokenTypes.STRING_CONST:
            string_val = self.tokenizer.string_val()
            self.write_string(string_val)
        elif token_type == TokenTypes.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword not in [
                Keywords.TRUE,
                Keywords.FALSE,
                Keywords.NULL,
                Keywords.THIS,
            ]:
                self.raise_error("表达式有误")
            self.write_keyword(keyword)
        elif token_type == TokenTypes.SYMBOL:
            symbol = self.tokenizer.symbol()
            if symbol == "(":
                self.write_symbol(symbol)
                self.compile_expression()
                symbol = self.get_symbol("符号')'")
                if symbol != ")":
                    self.raise_error("缺少符号')'")
                self.write_symbol(symbol)
            elif symbol in ["-", "~"]:
                self.write_symbol(symbol)
                self.compile_term()
            else:
                self.raise_error("符号错误")
            pass
        elif token_type == TokenTypes.IDENTIFIER:
            identifier = self.tokenizer.identifier()
            self.write_identifier(identifier)
            # 预读取分析
            if self.tokenizer.has_more_tokens():
                token = self.tokenizer.inadvance()
                token_type = self.tokenizer.token_type(token)
                if token_type == TokenTypes.SYMBOL:
                    symbol = self.tokenizer.symbol(token)
                    if symbol == "[":
                        # [
                        symbol = self.get_symbol()
                        self.write_symbol(symbol)
                        # 表达式
                        self.compile_expression()
                        # ]
                        symbol = self.get_symbol()
                        if symbol != "]":
                            self.raise_error("缺少符号']'")
                        self.write_symbol(symbol)
                        pass
                    elif symbol in ["(", "."]:
                        # . 或 (
                        symbol = self.get_symbol("符号'('")
                        if symbol == ".":
                            # .
                            self.write_symbol(symbol)
                            # 函数名
                            identifier = self.get_identifier("函数名")
                            self.write_identifier(identifier)
                            # (
                            symbol = self.get_symbol("符号'('")
                        # (
                        if symbol != "(":
                            self.raise_error("缺少符号'('")
                        self.write_symbol(symbol)
                        # 表达式列表
                        self.compile_expression_list()
                        # )
                        symbol = self.get_symbol("符号')'")
                        if symbol != ")":
                            self.raise_error("缺少符号')'")
                        self.write_symbol(symbol)
                        pass

        self.write_closing_tag(tag)
        pass

    def compile_expression_list(self):
        """
        编译由逗号分隔的表达式列表（可能为空）
        """
        tag = "expressionList"
        self.write_opening_tag(tag)
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
            self.write_symbol(symbol)
        self.write_closing_tag(tag)
        pass

    def get_keyword(self, comment: str = None) -> Keywords:
        token_type = self.get_token_type()
        if token_type != TokenTypes.KEYWORD:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.keyword()

    def get_symbol(self, comment: str = None) -> str:
        token_type = self.get_token_type(comment)
        if token_type != TokenTypes.SYMBOL:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.symbol()

    def get_identifier(self, comment: str = None) -> str:
        token_type = self.get_token_type(comment)
        if token_type != TokenTypes.IDENTIFIER:
            self.raise_error(f"缺少{comment}")
        return self.tokenizer.identifier()

    def get_token_type(self, comment: str = None) -> TokenTypes:
        if not self.tokenizer.has_more_tokens():
            self.raise_error(f"缺少{comment}")
        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        return token_type

    def raise_error(self, err: str, line_num: int = -1):
        pre = ""
        if line_num == -1:
            if self.tokenizer.token != None:
                line_num = self.tokenizer.token.line + 1
                pre = f"{self.tokenizer.token.txt} 附近"
            else:
                line_num = 1
        raise ValueError(f"行：{line_num}，{pre}，{err}")

    def write_keyword(self, keyword: Keywords):
        self.lines.append(f"<keyword>{keyword.name.lower()}</keyword>")
        pass

    def write_symbol(self, symbol: str):
        symbol = symbol.replace("&", "&amp;")
        symbol = symbol.replace("<", "&lt;")
        symbol = symbol.replace(">", "&gt;")
        self.lines.append(f"<symbol>{symbol}</symbol>")
        pass

    def write_identifier(self, identifier: str):
        self.lines.append(f"<identifier>{identifier}</identifier>")
        pass

    def write_int(self, val: int):
        self.lines.append(f"<integerConstant>{val}</integerConstant>")
        pass

    def write_string(self, val: str):
        val = val.replace("&", "&amp;")
        val = val.replace("<", "&lt;")
        val = val.replace(">", "&gt;")
        self.lines.append(f"<stringConstant>{val}</stringConstant>")
        pass

    def write_opening_tag(self, tag: str):
        self.lines.append(f"<{tag}>")
        pass

    def write_closing_tag(self, tag: str):
        self.lines.append(f"</{tag}>")
        pass

    def write_xml(self):
        with open(self.xml_path, "w") as file_obj:
            for line in self.lines:
                file_obj.write(f"{line}\r\n")
        pass

    pass
