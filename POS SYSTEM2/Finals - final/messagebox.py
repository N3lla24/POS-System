from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

class Message():
    def __init__(self) -> None:
        pass
    
    def showmessagebox(self, title, output_txt):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(output_txt)
        icon = QIcon()
        icon.addPixmap(QPixmap("C:\POS SYSTEM2\Finals - final\images\Picsart_23-06-15_09-41-02-215.png"), QIcon.Normal, QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
