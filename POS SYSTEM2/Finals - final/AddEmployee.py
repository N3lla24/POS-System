from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets, uic
from messagebox import Message
import psycopg2
import psycopg2.extras

class AddEmployeeAdmin(QDialog):
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed  
    def __init__(self, parent=None):
        super(AddEmployeeAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\AddEmployee.ui", self)
        self.show()
        
        self.messagebox = Message()

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 800
        height = 529
        self.resize(width, height)
        self.setFixedSize(width, height)
        self.Cancel.clicked.connect(self.exit_edit)
        self.AddNew.clicked.connect(self.add_prod)

    def exit_edit(self):
        self.close()

    def add_prod(self):
        if self.radioButton.isChecked():
            self.new_is_cas = True
        elif self.radioButton_2.isChecked():
            self.new_is_cas = False
        else:
            self.new_is_cas = None 
            
        if self.addEmpFName.text() == "" or self.AddEmpLName.text() == "":
            self.messagebox.showmessagebox("Incomplete Employee Name Inputted", "Input Employee Name First!\t\t")
        elif self.new_is_cas is None:
            self.messagebox.showmessagebox("Employee Designation Not Assigned", "Designate Employee First!\t\t")
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
                insert_script = 'INSERT INTO STAFF(STAFF_LNAME, STAFF_FNAME, STAFF_IS_CAS) VALUES (%s, %s, %s)'
                insert_value = (self.AddEmpLName.text(), self.addEmpFName.text(), self.new_is_cas)
                cur.execute(insert_script, insert_value)
                conn.commit()
            except Exception as error:
                self.messagebox.showmessagebox("Adding Employee Error", "Adding New Employee is not Successful!\t\t")
            finally:
                if conn is not None:
                    cur.close()
                    conn.close()
                    self.close()
        
    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()


def main():
    app = QApplication([])
    window = AddEmployeeAdmin()
    app.exec()

if __name__ == '__main__':
    main()