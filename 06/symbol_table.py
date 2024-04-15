class SymbolTable:
    """
    在符号标签和数字地址之间建立关联
    """

    def __init__(self) -> None:
        self.dics = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        for i in range(16):
            self.dics[f"R{i}"] = i
        pass

    def add_entry(self, symbol: str, address: int):
        """
        将（symbol,address）配对加入符号表\n
        参数：
            symbol：符号标签\n
            address：数字地址\n
        """
        self.dics[symbol] = address
        pass

    def contains(self, symbol: str) -> bool:
        """
        符号表是否包含了指定的symbol\n
        参数：
            symbol：符号标签\n
        返回：
            包含，返回true；否则，返回false
        """
        return symbol in self.dics.keys()

    def get_address(self, symbol: str) -> int:
        """
        返回与symbol关联的地址\n
        参数：
            symbol：符号标签\n
        返回：
            与symbol关联的数字地址
        """
        return self.dics[symbol]

    pass
