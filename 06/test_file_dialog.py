from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        button = QPushButton("Save File")
        button.clicked.connect(self.open_save_dialog)
        self.setCentralWidget(button)
 
    def open_save_dialog(self):
        file_dialog = QFileDialog(filter="asm (*.asm);;hack(*.hack);;所有文件(*)")
        file_dialog.setDefaultSuffix(".hack")  # 设置默认文件名后缀为.txt
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setLabelText(QFileDialog.DialogLabel.FileName, "Max.hack")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)  # 设置对话框为保存模式
        file_dialog.setDirectory('06/max')
        file_dialog.setWindowTitle("Save File")
        # file_dialog.setNameFilter('Max.hack')
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            print(f"Selected file: {selected_file}")
 
app = QApplication([])
window = MainWindow()
window.show()
app.exec()