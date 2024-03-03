from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, uic

class DeleteProductAdmin(QDialog):  
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed
    def __init__(self, parent=None):
        super(DeleteProductAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\DeleteProduct.ui", self)
        self.show()

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 500
        height = 240
        self.resize(width, height)
        self.setFixedSize(width, height)

        self.Cancel.clicked.connect(self.exit_edit)
        self.Confirm.clicked.connect(self.confirm_delete)
        
        self.confirmed = False

    def exit_edit(self):
        self.close()

    def confirm_delete(self):
        # add logic to delete/transfer or update the status of a product
        self.confirmed = True
        self.close()
        
    def get_confirmed(self):
        return self.confirmed
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()

def main():
    app = QApplication([])
    window = DeleteProductAdmin()
    app.exec()

if __name__ == '__main__':
    main()