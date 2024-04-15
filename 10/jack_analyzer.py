import logging
import os
import sys
import traceback
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine


class JackAnalyzer:
    """
    Jack语法分析器
    Jack语法分析器接收单一的命令行参数，如下所示：
    prompt> JackAnalyzer source
    source是行如Xxx.jack（扩展名是不要的）的文件名称
    或是包含若干个.jack文件的路径名（在这种情况下，没有扩展名）。语法分析器将Xxx.jack文件编译成名为Xxx.xml的文件，
    保存在与源文件相同的路径下。如果source是路径名，那么该路径下的每个.jack文件都将被编译，
    分别生成相应的.xml文件，保存在相同的路径下。
    """
    def __init__(self, args) -> None:
        try:
            self.translation(args[0])
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            logging.error("程序运行错误")
            logging.error(e)
            logging.error(traceback.format_exc())
        pass

    def translation(self, args1: str):
        """
        编译
        参数：
        args1(str)：jack文件路径或jack所在目录路径
        """
        jack_folder = ""
        jack_files: list[str] = []
        if args1.endswith(".jack"):
            jack_file = os.path.basename(args1)
            jack_files.append(jack_file)
            jack_folder = args1[0 : -len(jack_file)]
            pass
        else:
            jack_folder = args1
            file_names = os.listdir(jack_folder)
            for file_name in file_names:
                if file_name.endswith(".jack"):
                    jack_files.append(file_name)
            pass
        
        for jack_file in jack_files:
            success,err = self.parse_jack_file(jack_folder, jack_file)
            if not success:
                logging.error(err)
                logging.error(f"编译 {jack_file} 失败")
                break
            logging.info(f"编译 {jack_file} 完成")
        if success:
            print("编译完成")
            logging.info(f"全部编译成功")
        pass

    def parse_jack_file(self, jack_folder: str, jack_file: str) -> tuple[bool,str]:
        """
        编译vm文件
        参数：
        jack_folder(str)：jack文件所在目录
        jack_file(str)：jack文件名
        返回值：
        bool：编译成功，返回true；否则，返回false和错误信息
        """
        logging.info(f"编译 {jack_file} 开始")
        jack_name, jack_suffix = os.path.splitext(jack_file)
        
        try:
            tokenizer = JackTokenizer(f"{jack_folder}/{jack_file}")
            # engine = CompilationEngine(tokenizer, f"{jack_folder}/{jack_name}.xml")
            engine = CompilationEngine(tokenizer, f"{jack_folder}/{jack_name}_MY.xml")
            engine.compile_class()
            return (True, None)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            return (False, value)
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
        JackAnalyzer(args)
    else:
        logging.error("所传参数错误")
    logging.debug("程序退出")
    pass


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])