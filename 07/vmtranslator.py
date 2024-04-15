import logging
import os
import sys
import traceback
from vm_parser import VmParser
from code_writer import CodeWriter
from command_types import CommandTypes


class Vmtranslator:
    """
    VM翻译器\n
    VM翻译器可以接收一个简单的单一命令行参数，如下：
    Prompt> Vmtranslator source
    这里source是Xxx.vm文件的文件名（必须有扩展名）
    或者是包含一个或多个.vm文件的路径名称（不能带扩展名）。
    翻译的结果通常是生成一个单一的名为Xxx.asm的汇编语言文件，保存在与Xxx.vm相同的路径下。
    翻译的代码必须符合Hack平台上的标准VM映射规则。
    """

    def __init__(self, args) -> None:
        self.translation(args[0])
        pass

    def translation(self, args1: str):
        vm_folder = ""
        vm_files: list[str] = []
        asm_name = ""
        if args1.endswith(".vm"):
            vm_file = os.path.basename(args1)
            vm_files.append(vm_file)
            vm_folder = args1[0 : -len(vm_file)]
            vm_name, vm_suffix = os.path.splitext(vm_file)
            asm_name = vm_name
            pass
        else:
            vm_folder = args1
            file_names = os.listdir(vm_folder)
            for file_name in file_names:
                if file_name.endswith(".vm"):
                    vm_files.append(file_name)
            asm_name = os.path.basename(vm_folder)
            pass
        self.code_writer = CodeWriter(f"{vm_folder}/{asm_name}.asm")
        for vm_file in vm_files:
            success = self.parse_vm_file(vm_folder, vm_file)
            if not success:
                break
        self.code_writer.close()
        if success:
            print("编译完成")
            logging.info(f"编译文件{asm_name}.asm成功")
        pass

    def parse_vm_file(self, vm_folder: str, vm_file: str) -> bool:
        with open(f"{vm_folder}/{vm_file}", "r") as vm_obj:
            lines = vm_obj.readlines()
        vm_parser = VmParser(lines)
        self.code_writer.set_file_name(vm_file[:-3])

        total = len(vm_parser.lines)
        trans_success = True
        while vm_parser.has_more_commands():
            line_num = vm_parser.next_line_index + 1
            success, data = self.vm_to_asm(vm_parser)
            if not success:
                trans_success = False
                msg = f"{vm_file} {data}"
                print(f"\n{msg}")
                logging.error(msg)
                break
            print(f"\r{vm_file} {line_num}/{total}", end="")
        return trans_success

    def vm_to_asm(self, vm_parser: VmParser) -> tuple[bool, str]:
        """
        编译下一行程序\n
        返回：
            bool：成功，返回True；否则，返回False\n
            str：成功，None；否则，错误信息
        """
        line_num = vm_parser.next_line_index + 1
        try:
            vm_parser.advance()
            command_type = vm_parser.command_type()
            match command_type:
                case CommandTypes.C_ARITHMETIC:
                    self.code_writer.write_arithmetic(vm_parser.arg1())
                case CommandTypes.C_POP | CommandTypes.C_PUSH:
                    segment = vm_parser.arg1()
                    if segment == None:
                        raise ValueError('段名参数不能为空')
                    index = vm_parser.arg2()
                    self.code_writer.write_push_pop(command_type, segment, index)
                case CommandTypes.ERROR:
                    raise ValueError("语法错误")
            return (True, None)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            return (False, f"{line_num}行，{value}")

    pass


def main(args=None):
    logging.basicConfig(
        filename=f"{__file__[:-3]}.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )
    logging.debug("程序启动")
    if len(args) > 0:
        Vmtranslator(args)
    else:
        logging.error("所传参数错误")
    logging.debug("程序退出")
    pass


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])
