from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from messagebox import Message
from OrderStack import Singly

class CashierCalc(QDialog):
    continueClicked = pyqtSignal()

    def __init__(self, parent=None):
        super(CashierCalc, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\CashierCalculator.ui", self)
        self.show()

        screen = QApplication.desktop().screenGeometry()
        width = 800
        height = 885
        self.resize(width, height)
        self.setFixedSize(width, height)
        self.stack = Singly()
        
        self.messagebox = Message()
        self.GenRecButton.clicked.connect(self.check_data)
        self.numberbtngroup = QButtonGroup()
        self.numberbtngroup.addButton(self.Button0, 0)
        self.numberbtngroup.addButton(self.Button1, 1)
        self.numberbtngroup.addButton(self.Button2, 2)
        self.numberbtngroup.addButton(self.Button3, 3)
        self.numberbtngroup.addButton(self.Button4, 4)
        self.numberbtngroup.addButton(self.Button5, 5)
        self.numberbtngroup.addButton(self.Button6, 6)
        self.numberbtngroup.addButton(self.Button7, 7)
        self.numberbtngroup.addButton(self.Button8, 8)
        self.numberbtngroup.addButton(self.Button9, 9)
        self.numberbtngroup.addButton(self.ButtonDot, 10)
        self.numberbtngroup.addButton(self.ButtonClear, 11)
        self.numberbtngroup.setExclusive(True)
        self.numberbtngroup.buttonClicked[int].connect(self.number_clicked)
        
        
    def to_receipt_details(self):
        # self.check_finished_calcu()
        self.continueClicked.emit()
        self.close()
        
    def number_clicked(self, id):
        for button in self.numberbtngroup.buttons():
            if button is self.numberbtngroup.button(id):
                self.CashReceived.setText(f'{self.CashReceived.text()}{button.text()}')
            if id == 11:
                self.CashReceived.setText("")
                
    def set_total_price(self, total_price):
        self.TotalPrice.setText(f'{self.TotalPrice.text()}{str(total_price)}')
                
    def get_total_price(self):
        totalprice = self.TotalPrice.text().split(":")
        return totalprice[1]
        
    def get_cash_received(self):
        return self.CashReceived.text()

    def get_customer_name(self):
        return self.CustomerName.text()
        
    def check_data(self):
        if self.CashReceived.text() == "" :
            self.messagebox.showmessagebox("No Cash Inputted", "Input Cash First!")
        elif self.CustomerName.text() == "":
            self.messagebox.showmessagebox("No Customer Name Inputted", "Input Customer Name First!")
        else:
            try:
                cash = float(self.CashReceived.text())
                if(cash < 0):
                    self.messagebox.showmessagebox("Negative Cash Inputted", "Input Valid Numbers Only!\t")
                elif(float(self.get_total_price()) > cash):
                    self.messagebox.showmessagebox("Insufficient Money Inputted", "Input Sufficient Money Only!\t")
                else:
                    self.GenRecButton.setText("Generate Receipt")
                    self.GenRecButton.clicked.connect(self.to_receipt_details)
            except Exception as error:
                self.messagebox.showmessagebox("Incorrect Cash Input Value", "Input Numbers Only!\t")
                
    # def check_finished_calcu(self):
    #     count = 0
    #     count += 1
    #     return count
        
   

def main():
    app = QApplication([])
    window = CashierCalc()
    app.exec_()

if __name__ == '__main__':
    main()
