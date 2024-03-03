from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QPushButton
from messagebox import Message
import psycopg2
import psycopg2.extras


class AddProductAdmin(QDialog):  
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed

    def __init__(self, parent=None):
        super(AddProductAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\AddProduct.ui", self)
        self.show()
        
        self.messagebox = Message()

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 800
        height = 549
        self.resize(width, height)
        self.setFixedSize(width, height)
        self.Cancelsub.clicked.connect(self.exit_edit)
        self.AddProductsub.clicked.connect(self.add_prod)
        
    def exit_edit(self):
        self.close()

    def add_prod(self):
        if self.addProductName.text() == "" or self.addProductPrice.text() == "":
            self.messagebox.showmessagebox("Incomplete Form", "Input Needed Ingredients Details First!")
        else:
            try:
                price = float(self.addProductPrice.text())
                if(price < 0):
                    self.messagebox.showmessagebox("Negative Product Price Inputted", "Input Valid Product Price Only!\t")
                elif price == 0.00:
                    self.messagebox.showmessagebox("No Product Price Inputted", "Input Valid Product Price Only!\t")
                else:
                    # add logic to insert new employee to table
                    try: 
                        conn = psycopg2.connect(
                            host = "localhost",
                            dbname ='cafe',
                            user = 'postgres',
                            password = '171220',
                            port = 5432)
                        cur = conn.cursor()
                        insert_script = 'INSERT INTO PRODUCT(PROD_NAME, PROD_PRICE, PROD_STAT) VALUES (%s, %s, %s)'
                        insert_value = (self.addProductName.text(), float(self.addProductPrice.text()), 1)
                        cur.execute(insert_script, insert_value)
                        conn.commit()
                    except Exception as error:
                        self.messagebox.showmessagebox("Adding Product Error", "Adding New Product is not Successful!\t\t")
                    finally:
                        if conn is not None:
                            cur.close()
                            conn.close()
                            self.close()
            except Exception as error:
                self.messagebox.showmessagebox("Incorrect Product Price Value", "Input Numbers Only!\t")
        
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()


def main():
    app = QApplication([])
    window = AddProductAdmin()
    app.exec()

if __name__ == '__main__':
    main()