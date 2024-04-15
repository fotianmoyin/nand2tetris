import logging
import pathlib
import sys
import traceback
from typing import Dict
from PySide6.QtCore import (
    QObject,
    Slot,
    QThread,
    Signal,
    QThreadPool,
    Qt,
    QLocale,
    QSize,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QWidget,
    QDialog,
)
from PySide6.QtGui import QBrush, QColor
from main_window_ui import Ui_MainWindow
from about_dialog_ui import Ui_AboutDialog
from asm_parser import AsmParser
from command_types import CommandTypes
from asm_code import AsmCode
from symbol_table import SymbolTable
import os
from threading import Thread
import time
from worker import Worker


class AssemblerGUI(QMainWindow, Ui_MainWindow):
    """
    汇编编译器
    """

    def __init__(self):
        super(AssemblerGUI, self).__init__()
        self.setupUi(self)
        # 添加状态栏控件
        # self.le_status = QLineEdit()
        # self.le_status.setReadOnly(True)
        # self.le_status.setFocusPolicy(Qt.NoFocus)
        # self.statusBar().addWidget(self.le_status, 1)
        # 绑定事件
        self.closeEvent = self.on_close
        self.lsw_asm.currentRowChanged.connect(self.asm_item_changed)
        self.lsw_hack.currentRowChanged.connect(self.hack_item_changed)
        self.lsw_compare.currentRowChanged.connect(self.compare_item_changed)
        self.lsw_asm.itemClicked.connect(self.asm_item_changed)
        self.lsw_hack.itemClicked.connect(self.hack_item_changed)
        self.lsw_compare.itemClicked.connect(self.compare_item_changed)
        self.action_load_source_file.triggered.connect(self.load_source_file)
        self.action_save_destination_file.triggered.connect(self.save_destination_file)
        self.action_exit.triggered.connect(self.exit)
        self.action_single_step.triggered.connect(self.single_step)
        self.action_fast_forward.triggered.connect(self.fast_forward)
        self.action_stop.triggered.connect(self.stop)
        self.action_rewind.triggered.connect(self.rewind)
        self.action_fast_translation.triggered.connect(self.fast_translation)
        self.action_load_comparison_file.triggered.connect(self.load_comparison_file)
        self.action_about.triggered.connect(self.about)
        self.set_action_enable(load_source_file=True)
        # 翻译状态
        self.run_trans = False
        # 单步翻译
        self.as_single_step = False
        # 连续翻译
        self.as_fast_forward = False
        # 是否已加载比较代码
        self.compare_loaded = False
        self.trans_failed = False
        self.compare_failed = False
        self.asm_lines: list[str] = []
        self.hack_lines: list[str] = []
        self.compare_lines: list[str] = []
        # 对话框默认目录
        self.dialog_dir = "."
        # 线程池
        self.threadpool = QThreadPool()
        print(f"max thread count {self.threadpool.maxThreadCount()}")
        pass

    def on_close(self, event):
        logging.debug("程序退出")

    def worker_start(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        worker = Worker(self.worker_fn)
        worker.signals.result.connect(self.worker_result)
        worker.signals.finished.connect(self.worker_finished)
        worker.signals.progress.connect(self.worker_progress)

        # Execute
        # 使用线程池运行的程序无法调试，调试可在另外thread中运行worker.run()
        self.threadpool.start(worker)
        # thread = Thread(target=worker.run)
        # thread.start()
        pass

    def worker_fn(self, progress_callback):
        total = len(self.asm_lines)
        while self.asm_parser.has_more_commands():
            # 标记编译行
            if self.as_single_step or self.as_fast_forward:
                self.change_item(asm_index=self.asm_parser.next_line_index)
                pass

            # 编译程序
            success, data = self.asm_to_hack()
            if success:
                if data != "":
                    self.hack_lines.append(data)
                    self.lsw_hack.addItem(f"{data}")
                    trans = TransPair(
                        self.asm_parser.line_index, self.asm_parser.cmd_index
                    )
                    self.trans_list.add(trans)
                else:
                    self.trans_list.add(TransPair(self.asm_parser.line_index))
            else:
                self.trans_failed = True
                self.statusbar.showMessage(data)
                logging.error(data)
                break
            # 标记编译行
            if self.as_single_step or self.as_fast_forward:
                self.change_item(asm_index=self.asm_parser.line_index)
                pass

            # 显示进度
            line_num = self.asm_parser.line_index + 1
            n = (line_num) * 100 / total
            progress_callback.emit(n)
            self.statusbar.showMessage(f"{line_num}行，已完成：{n:.0f}%")

            # 比较代码
            if not self.compare(self.asm_parser.line_index):
                self.compare_failed = True
                err = f"{self.asm_parser.line_index+1}行，翻译后代码对比不一致"
                self.statusbar.showMessage(err)
                logging(err)
                break
            # 停止检查
            if not self.run_trans:
                break
            # 单步执行
            if self.as_single_step:
                break
            # 连续执行
            if self.as_fast_forward:
                time.sleep(0.5)
            pass

        self.run_trans = False
        if self.asm_parser.has_more_commands():
            self.set_action_enable(
                single_step=True,
                fast_forward=True,
                rewind=True,
                fast_translation=True,
            )
        else:
            self.set_action_enable(
                save_destination_file=True,
                rewind=True,
            )
            # 显示编译结果
            if self.compare_loaded and not self.compare_failed:
                self.statusbar.showMessage("编译完成并比较成功")
                pass
            else:
                self.statusbar.showMessage("编译完成")
                pass
            logging.debug(f"编译文件{self.asm_name}.asm成功")

        return "编译结束"

    def asm_to_hack(self) -> tuple[bool, str]:
        """
        编译下一行程序\n
        返回：
            bool：成功，返回True；否则，返回False\n
            str：成功，返回编译代码；否则，返回错误信息
        """
        line_num = self.asm_parser.next_line_index + 1
        try:
            hack_txt = ""
            self.asm_parser.advance()
            command_type = self.asm_parser.command_type()
            match command_type:
                case CommandTypes.A_COMMAND:
                    symbol = self.asm_parser.symbol()
                    address = 0
                    if symbol.isdigit():
                        # 数值地址
                        address = int(symbol)
                    else:
                        symbol = self.asm_parser.symbol()
                        # 名称规范检查
                        (success, err_msg) = self.name_check(symbol)
                        if not success:
                            raise ValueError(err_msg)
                        # 变量地址
                        if not self.symbol_table.contains(symbol):
                            self.symbol_table.add_entry(symbol, self.var_address)
                            self.var_address = self.var_address + 1
                        address = self.symbol_table.get_address(symbol)
                    hack_txt = f"0{address:015b}"
                case CommandTypes.C_COMMAND:
                    # dest域
                    symbol_dest = self.asm_parser.dest()
                    address_dest = self.asm_code.dest(symbol_dest)
                    if address_dest < 0:
                        raise ValueError("C指令dest域错误")
                    # comp域
                    symbol_comp = self.asm_parser.comp()
                    address_comp = self.asm_code.comp(symbol_comp)
                    if address_comp < 0:
                        raise ValueError("C指令comp域错误")
                    # jump域
                    symbol_jump = self.asm_parser.jump()
                    address_jump = self.asm_code.jump(symbol_jump)
                    if address_jump < 0:
                        raise ValueError("C指令jump域错误")
                    hack_txt = (
                        f"111{address_comp:07b}{address_dest:03b}{address_jump:03b}"
                    )
                case CommandTypes.L_COMMAND:
                    symbol = self.asm_parser.symbol()
                    (success, err_msg) = self.name_check(symbol)
                    if not success:
                        raise ValueError(err_msg)
                    pass
                case CommandTypes.ERROR:
                    raise ValueError("语法错误")
            return (True, hack_txt)
        except:
            exctype, value = sys.exc_info()[:2]
            return (False, f"{line_num}行，{value}")

    def name_check(self, symbol: str) -> tuple[bool, str]:
        """
        检查命名是否符合规范\n
        返回：
            bool：成功，返回True；否则，返回False\n
            str：成功，返回None；否则，返回错误信息
        """
        symbol = symbol.strip()
        if symbol == "":
            return (False, "名称不能为空")
        for c in symbol:
            if (
                c
                not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$:"
            ):
                return (False, f"名称不能包含符号'{c}'")
        if symbol[0] in "0123456789":
            return (False, "名称不能以数字开头")
        return (True, None)

    def compare(self, asm_index) -> bool:
        if not self.compare_loaded:
            return True

        trans = self.trans_list.get(asm_index=asm_index)
        if trans == None or trans.hack_index < 0:
            return True

        hack_index = trans.hack_index
        hack_max_index = len(self.hack_lines) - 1
        compare_max_index = len(self.compare_lines) - 1

        if hack_max_index >= hack_index and compare_max_index < hack_index:
            return False

        if hack_max_index < hack_index and compare_max_index >= hack_index:
            return False

        if hack_max_index < hack_index and compare_max_index < hack_index:
            return True

        if self.hack_lines[hack_index] != self.compare_lines[hack_index]:
            return False

        return True

    def worker_progress(self, n):
        print("\r进度：%d%%" % n, end="")

    def worker_result(self, s):
        print(f"\n{s}")

    def worker_finished(self):
        print("后台线程完成任务")

    def asm_item_changed(self, event):
        asm_index = self.lsw_asm.currentRow()
        self.change_item(asm_index=asm_index)
        pass

    def hack_item_changed(self, event):
        hack_index = self.lsw_hack.currentRow()
        self.change_item(hack_index=hack_index)
        pass

    def compare_item_changed(self, event):
        compare_index = self.lsw_compare.currentRow()
        self.change_item(hack_index=compare_index)
        pass

    def change_item(self, asm_index=-1, hack_index=-1):
        if asm_index >= 0:
            new_trans = self.trans_list.get(asm_index=asm_index)
            if new_trans == None:
                self.lsw_item_selected(self.lsw_asm, asm_index, True)
                self.lsw_clear_selected(self.lsw_hack)
                self.lsw_clear_selected(self.lsw_compare)
            else:
                self.lsw_item_selected(self.lsw_asm, new_trans.asm_index, True)
                self.lsw_item_selected(self.lsw_hack, new_trans.hack_index, True)
                self.lsw_item_selected(self.lsw_compare, new_trans.hack_index, True)
                pass
        elif hack_index >= 0:
            new_trans = self.trans_list.get(hack_index=hack_index)
            if new_trans == None:
                self.lsw_clear_selected(self.lsw_asm)
                self.lsw_clear_selected(self.lsw_hack)
            else:
                self.lsw_item_selected(self.lsw_asm, new_trans.asm_index, True)
                self.lsw_item_selected(self.lsw_hack, new_trans.hack_index, True)
                self.lsw_item_selected(self.lsw_compare, new_trans.hack_index, True)
                pass
        pass

    def lsw_clear_selected(self, lsw: QListWidget):
        for item in lsw.selectedItems():
            item.setSelected(False)

    def lsw_item_selected(self, lsw: QListWidget, index: int, select: bool):
        if lsw.count() <= 0:
            return
        if index < 0 or lsw.count() <= index:
            self.lsw_clear_selected(lsw)
            return
        lsw.item(index).setSelected(select)
        pass

    def set_action_enable(
        self,
        load_source_file=True,
        save_destination_file=False,
        single_step=False,
        fast_forward=False,
        stop=False,
        rewind=False,
        fast_translation=False,
        load_comparison_file=False,
    ):
        self.action_load_source_file.setEnabled(load_source_file)
        self.action_save_destination_file.setEnabled(save_destination_file)
        self.action_single_step.setEnabled(single_step)
        self.action_fast_forward.setEnabled(fast_forward)
        self.action_stop.setEnabled(stop)
        self.action_rewind.setEnabled(rewind)
        self.action_fast_translation.setEnabled(fast_translation)
        self.action_load_comparison_file.setEnabled(load_comparison_file)
        pass

    def load_source_file(self, event):
        # locale = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
        # QLocale.setDefault(locale)
        # QFileDialog.setLocale(locale)
        # QFileDialog.setProperty("locale", "zh_CN")
        asm_path, _ = QFileDialog.getOpenFileName(
            self, "选择汇编程序", self.dialog_dir, "汇编文件 (*.asm)"
        )
        if asm_path == "":
            return

        self.lsw_asm.clear()
        self.lsw_hack.clear()
        self.lsw_compare.clear()
        self.asm_lines.clear()
        self.hack_lines.clear()
        self.compare_lines.clear()
        self.compare_loaded = False
        self.trans_failed = False
        self.compare_failed = False

        asm_file = os.path.basename(asm_path)
        folder_path = asm_path[0 : -len(asm_file)]
        self.dialog_dir = folder_path
        stem, suffix = os.path.splitext(asm_file)
        self.asm_folder = folder_path
        self.asm_name = stem
        with open(asm_path) as file_object:
            self.asm_lines = file_object.readlines()
            pass

        for asm_line in self.asm_lines:
            line = asm_line.replace("\r", "")
            line = line.replace("\n", "")
            self.lsw_asm.addItem(line)

        self.symbol_table = SymbolTable()
        self.asm_code = AsmCode()
        self.var_address = 16
        # 遍历伪指令
        self.asm_parser = AsmParser(self.asm_lines)
        while self.asm_parser.has_more_commands():
            self.asm_parser.advance()
            if self.asm_parser.command_type() != CommandTypes.L_COMMAND:
                continue
            symbol = self.asm_parser.symbol()
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.asm_parser.next_cmd_index)
                pass
            pass
        self.asm_parser = AsmParser(self.asm_lines)
        self.trans_list = TransList()
        self.set_action_enable(
            single_step=True,
            fast_forward=True,
            rewind=True,
            fast_translation=True,
            load_comparison_file=True,
        )
        pass

    def save_destination_file(self, event):
        hack_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            f"{self.asm_folder}",
            "机器代码 (*.hack);;所有文件 (*)",
        )
        if hack_path == "":
            return

        # dlg = QMessageBox(self)
        # dlg.setWindowTitle("询问")
        # dlg.setText("文件已存在，是否覆盖？")
        # dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # dlg.setIcon(QMessageBox.Question)
        # button = dlg.exec()
        # if button != QMessageBox.Yes:
        #     return

        with open(hack_path, "w") as hack_object:
            for line in self.hack_lines:
                hack_object.write(f"{line}\r\n")
        pass

    def exit(self):
        self.close()
        pass

    def single_step(self, event):
        if self.trans_failed or self.compare_failed:
            return

        self.set_action_enable(
            single_step=True,
            fast_forward=True,
            rewind=True,
            fast_translation=True,
        )
        self.start_trans_worker(as_single_step=True)
        pass

    def fast_forward(self, event):
        if self.trans_failed or self.compare_failed:
            return

        self.set_action_enable(load_source_file=False, stop=True)
        self.start_trans_worker(as_fast_forward=True)
        pass

    def stop(self, event):
        self.run_trans = False
        pass

    def rewind(self, event):
        for item in self.lsw_asm.selectedItems():
            item.setSelected(False)

        self.asm_parser = AsmParser(self.asm_lines)
        self.trans_list = TransList()
        self.lsw_hack.clear()
        self.hack_lines.clear()
        self.set_action_enable(
            single_step=True,
            fast_forward=True,
            rewind=True,
            fast_translation=True,
            load_comparison_file=True,
        )
        self.statusbar.clearMessage()
        self.trans_failed = False
        self.compare_failed = False
        pass

    def fast_translation(self, event):
        if self.trans_failed or self.compare_failed:
            return

        self.set_action_enable(load_source_file=False, stop=True)
        self.start_trans_worker()
        pass

    def start_trans_worker(self, as_single_step=False, as_fast_forward=False):
        self.as_single_step = as_single_step
        self.as_fast_forward = as_fast_forward
        self.run_trans = True
        self.worker_start()
        pass

    def load_comparison_file(self, event):
        hack_path, _ = QFileDialog.getOpenFileName(
            self, "选择比较文件", self.dialog_dir, "机器代码 (*.hack)"
        )
        if hack_path == "":
            return

        self.compare_lines.clear()
        self.lsw_compare.clear()

        with open(hack_path) as file_object:
            lines = file_object.readlines()
            pass

        for line in lines:
            line = line.strip()
            self.lsw_compare.addItem(line)
            self.compare_lines.append(line)
        self.compare_loaded = True
        self.compare_failed = False
        pass

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.show(self)
        pass

    pass


class AboutDialog(QDialog, Ui_AboutDialog):
    """
    关于对话框
    """

    def __init__(self):
        super(AboutDialog, self).__init__()
        self.setupUi(self)
        pass

    def show(self, parent: QMainWindow):
        self.setFixedSize(QSize(self.width(), self.height()))
        parent_rect = parent.geometry()
        self_rect = self.geometry()
        self.move(parent_rect.center() - self_rect.center())
        self.exec()
        pass

    pass


class TransPair:
    def __init__(self, asm_index, hack_index=-1) -> None:
        self.asm_index: int = asm_index
        self.hack_index: int = hack_index
        pass


class TransList:
    def __init__(self) -> None:
        self.trans_dics: Dict[int, TransPair] = {}
        pass

    def clear(self):
        self.trans_dics.clear()
        pass

    def add(self, trans: TransPair):
        if trans.asm_index in self.trans_dics.keys():
            return
        self.trans_dics[trans.asm_index] = trans
        pass

    def get(self, asm_index=-1, hack_index=-1) -> TransPair:
        if asm_index != -1:
            trans = self.trans_dics.get(asm_index, None)
            return trans
        if hack_index != -1:
            for trans in self.trans_dics.values():
                if trans.hack_index == hack_index:
                    return trans
        return None

    def select(self, trans: TransPair):
        self.trans_selected = trans
        pass


class AssemblerCli:
    def __init__(self, args) -> None:
        self.translation(args[0])
        pass

    def translation(self, asm_path):
        # 加载汇编程序
        asm_file = os.path.basename(asm_path)
        folder_path = asm_path[0 : -len(asm_file)]
        asm_name, asm_suffix = os.path.splitext(asm_file)
        with open(asm_path) as file_object:
            lines = file_object.readlines()
            pass
        self.symbol_table = SymbolTable()
        self.asm_code = AsmCode()
        # 遍历伪指令
        self.asm_parser = AsmParser(lines)
        while self.asm_parser.has_more_commands():
            self.asm_parser.advance()
            if self.asm_parser.command_type() != CommandTypes.L_COMMAND:
                continue
            symbol = self.asm_parser.symbol()
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.asm_parser.next_cmd_index)
                pass
            pass
        # 编译汇编代码
        self.asm_parser = AsmParser(lines)
        self.var_address = 16
        hack_path = f"{folder_path}{asm_name}.hack"
        trans_success = True
        with open(hack_path, "w") as hack_object:
            total = len(self.asm_parser.lines)
            while self.asm_parser.has_more_commands():
                line_num = self.asm_parser.next_line_index + 1
                success, data = self.asm_to_hack()
                if not success:
                    trans_success = False
                    print(f"\n{data}")
                    logging.error(data)
                    break
                if data != "":
                    hack_object.write(f"{data}\r\n")
                print(f"\r{line_num}/{total}", end="")
        if self.asm_parser.has_more_commands():
            print("\n编译失败")
            logging.error(f"编译文件{asm_name}.asm失败")
        elif trans_success:
            print("\n编译成功")
            logging.error(f"编译文件{asm_name}.asm成功")
        pass

    def asm_to_hack(self) -> tuple[bool, str]:
        """
        编译下一行程序\n
        返回：
            bool：成功，返回True；否则，返回False\n
            str：成功，返回编译代码；否则，返回错误信息
        """
        line_num = self.asm_parser.next_line_index + 1
        try:
            hack_txt = ""
            self.asm_parser.advance()
            command_type = self.asm_parser.command_type()
            match command_type:
                case CommandTypes.A_COMMAND:
                    symbol = self.asm_parser.symbol()
                    address = 0
                    if symbol.isdigit():
                        # 数值地址
                        address = int(symbol)
                    else:
                        symbol = self.asm_parser.symbol()
                        # 名称检查
                        (success, err_msg) = self.name_check(symbol)
                        if not success:
                            raise ValueError(err_msg)
                        # 变量地址
                        if not self.symbol_table.contains(symbol):
                            self.symbol_table.add_entry(symbol, self.var_address)
                            self.var_address = self.var_address + 1
                        address = self.symbol_table.get_address(symbol)
                    hack_txt = f"0{address:015b}"
                case CommandTypes.C_COMMAND:
                    # dest域解析
                    symbol_dest = self.asm_parser.dest()
                    address_dest = self.asm_code.dest(symbol_dest)
                    if address_dest < 0:
                        raise ValueError("C指令dest域错误")
                    # comp域解析
                    symbol_comp = self.asm_parser.comp()
                    address_comp = self.asm_code.comp(symbol_comp)
                    if address_comp < 0:
                        raise ValueError("C指令comp域错误")
                    # jump域解析
                    symbol_jump = self.asm_parser.jump()
                    address_jump = self.asm_code.jump(symbol_jump)
                    if address_jump < 0:
                        raise ValueError("C指令jump域错误")
                    hack_txt = (
                        f"111{address_comp:07b}{address_dest:03b}{address_jump:03b}"
                    )
                case CommandTypes.L_COMMAND:
                    symbol = self.asm_parser.symbol()
                    (success, err_msg) = self.name_check(symbol)
                    if not success:
                        raise ValueError(err_msg)
                    pass
                case CommandTypes.ERROR:
                    raise ValueError("语法错误")
            return (True, hack_txt)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            return (False, f"{line_num}行，{value}")

    def name_check(self, symbol: str) -> tuple[bool, str]:
        """
        检查命名是否符合规范\n
        返回：
            bool：成功，返回True；否则，返回False\n
            str：成功，返回None；否则，返回错误信息
        """
        symbol = symbol.strip()
        if symbol == "":
            return (False, "名称不能为空")

        for c in symbol:
            if (
                c
                not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.$:"
            ):
                return (False, f"名称不能包含符号'{c}'")

        if symbol[0] in "0123456789":
            return (False, "名称不能以数字开头")

        return (True, None)

    pass


def main(args=None):
    logging.basicConfig(
        filename=f"{__file__[:-3]}.log",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )
    logging.debug("程序启动")
    # logging.debug('debug')
    # logging.info('info')
    # logging.warning('warning')
    # logging.error('error')
    # logging.critical('critical')
    if len(args) > 0:
        AssemblerCli(args)
        logging.debug("程序退出")
        return

    app = QApplication(sys.argv)
    # 设置应用程序的语言为中文
    # app.setProperty("locale", "zh_CN")
    win = AssemblerGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])
