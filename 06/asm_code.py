class AsmCode:
    """
    将Hack汇编语言助记符翻译成二进制码。
    """

    def __init__(self) -> None:
        pass

    def dest(self, mnemonic: str) -> int:
        """
        返回dest助记符的二进制码\n
        参数：
            mnemonic：dest助记符\n
        返回：
            int(3 bits)：dest助记符的二进制码；没有匹配，返回-1
        """
        match mnemonic:
            case "Null":
                return 0b000
            case "M":
                return 0b001
            case "D":
                return 0b010
            case "MD" | "DM":
                return 0b011
            case "A":
                return 0b100
            case "AM" | "MA":
                return 0b101
            case "AD" | "DA":
                return 0b110
            case "AMD" | "ADM" | "DAM" | "DMA" | "MAD" | "MDA":
                return 0b111
        return -1

    def comp(self, mnemonic: str) -> int:
        """
        返回comp助记符的二进制码\n
        参数：
            mnemonic：comp助记符\n
        返回：
            int(7 bits)：comp助记符的二进制码；没有匹配，返回-1
        """
        match mnemonic:
            case "0":
                return 0b0101010
            case "1":
                return 0b0111111
            case "-1":
                return 0b0111010
            case "D":
                return 0b0001100
            case "A":
                return 0b0110000
            case "M":
                return 0b1110000
            case "!D":
                return 0b0001101
            case "!A":
                return 0b0110001
            case "!M":
                return 0b1110001
            case "-D":
                return 0b0001111
            case "-A":
                return 0b0110011
            case "-M":
                return 0b1110011
            case "D+1":
                return 0b0011111
            case "A+1":
                return 0b0110111
            case "M+1":
                return 0b1110111
            case "D-1":
                return 0b0001110
            case "A-1":
                return 0b0110010
            case "M-1":
                return 0b1110010
            case "D+A":
                return 0b0000010
            case "D+M":
                return 0b1000010
            case "D-A":
                return 0b0010011
            case "D-M":
                return 0b1010011
            case "A-D":
                return 0b0000111
            case "M-D":
                return 0b1000111
            case "D&A":
                return 0b0000000
            case "D&M":
                return 0b1000000
            case "D|A":
                return 0b1010101
            case "D|M":
                return 0b1010101
        return -1

    def jump(self, mnemonic: str) -> int:
        """
        返回jump助记符的二进制码\n
        参数：
            mnemonic：jump助记符\n
        返回：
            int(3 bits)：jump助记符的二进制码；没有匹配，返回-1
        """
        match mnemonic:
            case "null":
                return 0b000
            case "JGT":
                return 0b001
            case "JEQ":
                return 0b010
            case "JGE":
                return 0b011
            case "JLT":
                return 0b100
            case "JNE":
                return 0b101
            case "JLE":
                return 0b110
            case "JMP":
                return 0b111
        return -1

    pass
