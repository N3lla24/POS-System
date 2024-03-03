from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtCore

class SignOutConfirm(QDialog):
    continueClicked = pyqtSignal()
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed

    def __init__(self, parent=None):
        super(SignOutConfirm, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\SignOutConfirmation.ui", self)
        self.show()

        screen = QApplication.desktop().screenGeometry()
        width = 800
        height = 477
        self.resize(width, height)
        self.setFixedSize(width, height)

        self.CashierSOCancel.clicked.connect(self.to_close)
        self.CashierSOConfirm.clicked.connect(self.emitContinueClicked)
    
    def to_close(self):
        self.close()

    def emitContinueClicked(self):
        self.continueClicked.emit()
        self.close()
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()
        

def main():
    app = QApplication([])
    window = SignOutConfirm()
    app.exec_()

if __name__ == '__main__':
    main()
