from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, uic
from messagebox import Message
import psycopg2
import psycopg2.extras

class EditEmployeeAdmin(QDialog): 
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed 
    def __init__(self, parent=None):
        super(EditEmployeeAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\EditEmployee.ui", self)
        self.show()
        
        self.messagebox = Message()

        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 800
        height = 579
        self.resize(width, height)
        self.setFixedSize(width, height)
    
        self.Cancel.clicked.connect(self.exit_edit)
        self.Save.clicked.connect(self.save_edit)
 
    def exit_edit(self):
        self.close()

    def save_edit(self):
        if self.radioButton.isChecked():
            self.new_is_cas = True
        elif self.radioButton_2.isChecked():
            self.new_is_cas = False
        else:
            self.new_is_cas = None
            
        if self.editEmpFNum.text() == "" or self.editEmpFName.text() == "" or self.editEmpLName.text() == "":
            self.messagebox.showmessagebox("Incomplete Form", "Input Needed Employee Details First!")
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
                insert_script = 'UPDATE STAFF SET STAFF_LNAME = %s, STAFF_FNAME = %s, STAFF_IS_CAS = %s WHERE STAFF_NUM = %s'
                insert_value = (self.editEmpLName.text(), self.editEmpFName.text(), self.new_is_cas, int(self.editEmpFNum.text()))
                cur.execute(insert_script, insert_value)
                conn.commit()
            except Exception as error:
                self.messagebox.showmessagebox("Employee Edit Error", "Editing the Employee is not Successful!\t\t")
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
    window = EditEmployeeAdmin()
    app.exec()

if __name__ == '__main__':
    main()