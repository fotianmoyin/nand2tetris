import re
from token_types import TokenTypes
from keywords import Keywords


class Token:
    def __init__(self, line: int, txt: str) -> None:
        self.line = line
        self.txt = txt
        pass

    pass


class JackTokenizer:
    """
    JackTokenizer:
    从输入流中删除所有的注释和空格，
    并根据Jack语法的规则将输入流分解成Jack语言的字元（终结符）。
    """

    def __init__(self, jack_path: str, jack_name:str) -> None:
        """
        打开输入文件/输入流，准备进行字元转换操作
        """
        self.keywords = [
            "class",
            "constructor",
            "function",
            "method",
            "field",
            "static",
            "var",
            "int",
            "char",
            "boolean",
            "void",
            "true",
            "false",
            "null",
            "this",
            "let",
            "do",
            "if",
            "else",
            "while",
            "return",
        ]
        self.symbols = [
            "{",
            "}",
            "(",
            ")",
            "[",
            "]",
            ".",
            ",",
            ";",
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
            "~",
        ]
        self.jack_name = jack_name;
        self.tokens = self.build_tokens(jack_path)
        # for token in self.tokens:
        #     print(f"{token.txt}")
        self.token: Token = None
        self.token_index = -1
        self.next_token: Token = None
        self.next_token_index = 0
        pass

    def build_tokens(self, jack_path: str) -> list[Token]:
        """
        从jack文件生成字元列表
        参数：
        jack_path(str):jack文件路径
        返回值：
        list[Token]:字元列表
        """
        with open(jack_path, "r") as jack_obj:
            lines = jack_obj.readlines()
        # 字元列表
        tokens: list[Token] = []
        comment_start = False
        for i in range(len(lines)):
            line = lines[i]
            if comment_start:
                # 多行注释结尾符检测
                comment_index = line.find("*/")
                if comment_index > -1:
                    # 多行注释结束
                    comment_start = False
                    line = line[comment_index + 2 :]
                else:
                    # 多行注释
                    continue
                pass
            # 去除//注释
            comment_index = line.find("//")
            if comment_index > -1:
                line = line[0:comment_index]
            # 去除/** */类注释
            line = re.sub("\/\*\*?[^*]+\*\/", " ", line)
            # 多行注释检测
            comment_index = line.find("/*")
            if comment_index > -1:
                comment_start = True
                line = line[0:comment_index]
                pass
            # 双引号字符串检测
            while True:
                # 双引号开头检测
                mark_index = line.find('"')
                if mark_index <= 0:
                    break
                # 分隔字符串到字元列表
                txts = self.token_split(line[0:mark_index])
                for txt in txts:
                    tokens.append(Token(i, txt))
                    pass
                # 双引号结束位置检测
                line = line[mark_index:]
                mark_index = line.find('"', 1)
                if mark_index <= 0:
                    self.raise_error("缺少双引号结尾符", i)
                # 将字符串添加到字元列表
                tokens.append(Token(i, line[0 : mark_index + 1]))
                line = line[mark_index + 1 :]
                pass
            # 分隔字符串到字元列表
            txts = self.token_split(line)
            for txt in txts:
                tokens.append(Token(i, txt))
            pass
        return tokens

    def token_split(self, line: str) -> list[str]:
        # 为符号前后添加空格，方便分隔
        line = line.replace("{", " { ")
        line = line.replace("}", " } ")
        line = line.replace("(", " ( ")
        line = line.replace(")", " ) ")
        line = line.replace("[", " [ ")
        line = line.replace("]", " ] ")
        line = line.replace(".", " . ")
        line = line.replace(",", " , ")
        line = line.replace(";", " ; ")
        line = line.replace("+", " + ")
        line = line.replace("-", " - ")
        line = line.replace("*", " * ")
        line = line.replace("/", " / ")
        line = line.replace("&", " & ")
        line = line.replace("|", " | ")
        line = line.replace("<", " < ")
        line = line.replace(">", " > ")
        line = line.replace("=", " = ")
        line = line.replace("~", " ~ ")
        # 将制表符转为空格
        line = line.replace("\t", " ")
        # 将多个空格转为单个
        line = re.sub(" +", " ", line)
        # 去除头尾空格
        line = line.strip()
        if line == "":
            return []
        txts = line.split(" ")
        return txts

    def has_more_tokens(self) -> bool:
        """
        输入中是否还有字元？
        返回值：
        bool：还有字元，返回true；否则，返回false
        """
        return len(self.tokens) - self.next_token_index >= 1

    def advance(self):
        """
        从输入中读取下一个字元，使其成为当前字元，
        该函数仅当has_more_tokens()返回为真时才能调用，
        最初始状态是没有当前字元
        """
        self.token = self.tokens[self.next_token_index]
        self.token_index = self.next_token_index
        self.next_token_index = self.next_token_index + 1

        pass

    def inadvance(self) -> Token:
        """
        提前查看下一字元
        返回值：
        TokenTypes:字元类型
        Token:字元
        """
        return self.tokens[self.next_token_index]

    def token_type(self, token: Token = None) -> TokenTypes:
        """
        返回当前字元的类型
        参数：
        token(Token):待分析字元
        返回值：
        TokenTypes:字元类型
        """
        if token == None:
            token = self.token
        if token.txt in self.keywords:
            return TokenTypes.KEYWORD
        if token.txt in self.symbols:
            return TokenTypes.SYMBOL
        if token.txt[0].isdigit():
            return TokenTypes.INT_CONST
        if token.txt.startswith('"'):
            return TokenTypes.STRING_CONST
        return TokenTypes.IDENTIFIER

    def keyword(self, token: Token = None) -> Keywords:
        """
        返回当前字元的关键字，仅当token_type()返回值为KEYWORD时才被调用
        参数：
        token(Token):待分析字元
        返回值：
        Keywords:关键字
        """
        if token == None:
            token = self.token

        match (token.txt):
            case "class":
                return Keywords.CLASS
            case "constructor":
                return Keywords.CONSTRUCTOR
            case "function":
                return Keywords.FUNCTION
            case "method":
                return Keywords.METHOD
            case "field":
                return Keywords.FIELD
            case "static":
                return Keywords.STATIC
            case "var":
                return Keywords.VAR
            case "int":
                return Keywords.INT
            case "char":
                return Keywords.CHAR
            case "boolean":
                return Keywords.BOOLEAN
            case "void":
                return Keywords.VOID
            case "true":
                return Keywords.TRUE
            case "false":
                return Keywords.FALSE
            case "null":
                return Keywords.NULL
            case "this":
                return Keywords.THIS
            case "let":
                return Keywords.LET
            case "do":
                return Keywords.DO
            case "if":
                return Keywords.IF
            case "else":
                return Keywords.ELSE
            case "while":
                return Keywords.WHILE
            case "return":
                return Keywords.RETURN
        pass

    def symbol(self, token: Token = None) -> str:
        """
        返回当前字元的字符，仅当token_type()的返回值为SYMBOL时才被调用
        参数：
        token(Token):待分析字元
        返回值：
        str:当前字元的字符
        """
        if token == None:
            token = self.token
        return token.txt

    def identifier(self, token: Token = None) -> str:
        """
        返回当前字元的标识符，仅当token_type()的返回值为IDENTIFIER时才被调用
        参数：
        token(Token):待分析字元
        返回值：
        str:当前字元的标识符
        """
        if token == None:
            token = self.token
        if token.txt[0].isdigit():
            self.raise_error("标识符不能以数字开头")
        return token.txt

    def int_val(self, token: Token = None) -> int:
        """
        返回当前字元的整数值，仅当token_type()的返回值为INT_CONST时才被调用
        参数：
        token(Token):待分析字元
        返回值：
        int:当前字元的整数值
        """
        if token == None:
            token = self.token
        value = int(token.txt)
        if value < 0 or value > 32767:
            self.raise_error("数值超出范围，jack允许的数值范围(0-32767)")
        return value

    def string_val(self, token: Token = None) -> str:
        """
        返回当前字元的字符串值，没有双引号。
        仅当token_type()的返回值为STRING_CONST时才被调用
        参数：
        token(Token):待分析字元
        返回值：
        str:当前字元的字符串值，没有双引号
        """
        if token == None:
            token = self.token
        if token.txt[-1] != '"':
            self.raise_error("字符串没有结束符")
        return token.txt[1: -1]

    def raise_error(self, err: str, line_num: int = -1):
        if line_num == -1:
            line_num = self.token.line + 1
        raise ValueError(f"行：{line_num}，{err}")

    pass
