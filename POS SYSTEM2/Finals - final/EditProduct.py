from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, uic
from messagebox import Message
import psycopg2
import psycopg2.extras

class EditProductAdmin(QDialog): 
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed 
    def __init__(self, parent=None):
        super(EditProductAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\EditProduct.ui", self)
        self.show()
        
        self.messagebox = Message()

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 800
        height = 549
        self.resize(width, height)
        self.setFixedSize(width, height)
    
        self.Cancel.clicked.connect(self.exit_edit)
        self.Save.clicked.connect(self.save_edit)  

    def exit_edit(self):
        self.close()

    def save_edit(self):
        # add logic to update the product details
        if self.newProductNum.text() == "" or self.newProductName.text() == "" or self.newProductPrice.text() == "":
            self.messagebox.showmessagebox("Incomplete Form", "Input Needed Ingredients Details First!")
        else:
            try:
                price = float(self.newProductPrice.text())
                if(price < 0):
                    self.messagebox.showmessagebox("Negative Product Price Inputted", "Input Valid Product Price Only!\t")
                else:
                    try:
                        conn = psycopg2.connect(
                            host = "localhost",
                            dbname ='cafe', 
                            user = 'postgres',
                            password = '171220',
                            port = 5432)
                        cur = conn.cursor()
                        insert_script = 'UPDATE PRODUCT SET PROD_NAME = %s, PROD_PRICE = %s  WHERE PROD_NUM = %s'
                        insert_value = (self.newProductName.text(), float(self.newProductPrice.text()), int(self.newProductNum.text()))
                        cur.execute(insert_script, insert_value)
                        conn.commit()
                    except Exception as error:
                        self.messagebox.showmessagebox("Editing Product Error", "Editing the Product is not Successful!\t\t")
                    finally:
                        if conn is not None:
                            cur.close()
                            conn.close()
                            self.close()
            except Exception as error:
                print(error)
                self.messagebox.showmessagebox("Incorrect Product Price Value", "Input Numbers Only!\t")
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()

def main():
    app = QApplication([])
    window = EditProductAdmin()
    app.exec()

if __name__ == '__main__':
    main()