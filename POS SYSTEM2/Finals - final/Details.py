from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtCore

class DetailsDialog(QDialog):
    continueClicked = pyqtSignal()
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed

    def __init__(self, parent=None):
        super(DetailsDialog, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\Details.ui", self)
        self.show()

        screen = QApplication.desktop().screenGeometry()
        width = 800
        height = 477
        self.resize(width, height)
        self.setFixedSize(width, height)
    
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()
        
def main():
    app = QApplication([])
    window = DetailsDialog()
    app.exec_()

if __name__ == '__main__':
    main()
