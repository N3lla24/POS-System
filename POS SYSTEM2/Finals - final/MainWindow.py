from PyQt5 import *
from PyQt5 import QtGui, QtWidgets, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from datetime import datetime
from SignOutConfirmation import SignOutConfirm
from Details import DetailsDialog
from CashierCalculator import CashierCalc
from AddProduct import AddProductAdmin
from DeleteProduct import DeleteProductAdmin
from EditProduct import EditProductAdmin
from EditEmployee import EditEmployeeAdmin
from AddEmployee import AddEmployeeAdmin
from EditIngredients import EditIngredientsAdmin
from AddIngredients import AddIngredientsAdmin
from OrderStack import Singly
from messagebox import Message
import win32print
import psycopg2
import psycopg2.extras

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\MainWindow.ui", self)
        self.show()

        screen = QApplication.desktop().screenGeometry()
        width = screen.width()
        height = screen.height()
        self.resize(width, height)
        self.setFixedSize(width, height)
        self.updateDateTime()
        
        self.stack = Singly()
        self.messagebox = Message()
        self.removeitemclicked = False
        
        self.staffid = 0
        self.staffname = ""
        self.cntcustomers = 0
        self.cntorders = 0
        self.alltransnum = 0

        self.stackedWidget.setCurrentWidget(self.mainSignIn)
        self.adminFunction.setCurrentWidget(self.editProduct)

        self.CashierButton.clicked.connect(self.to_cashier_signin)
        self.CashierToMain.clicked.connect(self.to_main)
        self.CashierSignInButton.clicked.connect(self.to_cashier_home)
        self.detailsPush.clicked.connect(self.to_details)
        
        self.addToListButton.clicked.connect(self.to_add_order_list)
        self.RemoveItemButton.clicked.connect(self.enable_delete_function)
        self.ConfirmButton.clicked.connect(self.to_calcu)
        self.ReceiptCancel.clicked.connect(self.cancelReceipt)
        self.ReceiptCancel.clicked.connect(self.to_cashier_home)
        self.ReceiptConfirm.clicked.connect(self.to_notice_print)
        self.returnedbtn.clicked.connect(self.to_returned_receipt)

        self.AdminButtn.clicked.connect(self.to_admin_signin)
        self.AdminToMain.clicked.connect(self.to_main)
        self.AdminSignInButton.clicked.connect(self.to_admin_home)
        self.adminDetails.clicked.connect(self.to_details)
        
        self.EditProductDetails.clicked.connect(self.to_edit_product)
        self.GenSalesReport.clicked.connect(self.to_gen_sales)
        self.ManageEmp.clicked.connect(self.to_manage_emp)
        self.ManageInv.clicked.connect(self.to_manage_inv)
        self.AddProduct.clicked.connect(self.to_add_product)
        self.DeleteProduct.clicked.connect(self.to_delete_product)
        self.EditProduct.clicked.connect(self.to_edit_productbtn)
        self.EditEmp.clicked.connect(self.to_edit_emp)
        self.AddEmp.clicked.connect(self.to_add_emp)
        self.EditIngredients.clicked.connect(self.to_edit_ing)
        self.AddItem.clicked.connect(self.to_add_ing)
        
        self.signOutPushButton.clicked.connect(self.to_signout_notice)
        
        self.adminSO.clicked.connect(self.to_signout_notice)
        
        self.menuitemgroup = QButtonGroup()
        self.menuitemgroup.setExclusive(True)
        self.menuitemgroup.buttonClicked[int].connect(self.show_order)
        self.orderitemgroup = QButtonGroup()
        self.orderitemgroup.setExclusive(True)
        self.orderitemgroup.buttonClicked[int].connect(self.delete_order)
        
        
    def to_cashier_signin(self):
        self.stackedWidget.setCurrentWidget(self.cashierSignIn)
    
    def to_cashier_home(self):
        success = False
        #Sign in
        try:
            with psycopg2.connect(
                    host="localhost",
                    dbname='cafe',
                    user='postgres',
                    password='171220',
                    port=5432) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute('SELECT * FROM STAFF WHERE STAFF_IS_CAS = TRUE')
                    for record in cur.fetchall():
                        if str(record['staff_num']) == self.CashierEmpNum.text():
                            if str(record['staff_pass']) == self.CashierPass.text():
                                success = True
                                self.staffid = int(record['staff_num'])
                                self.staffname = str(record['staff_lname']) + ", " + str(record['staff_fname'])
                                break
                        else:
                            success = False
        except Exception as error:
            self.messagebox.showmessagebox("No Database", "Database is Not Available!")
        finally:
            try:
                if conn is not None:
                    conn.close()
                if success:
                    self.addessential_details()
                    self.stackedWidget.setCurrentWidget(self.cashierHome)
                    self.cashierNum.setText("Cashier Staff Number: ")
                    self.cashierName.setText("Cashier Name: ")  
                    self.cashierNum.setText(f'{self.cashierNum.text()}{str(self.staffid)}')
                    self.cashierName.setText(f'{self.cashierName.text()}{str(self.staffname)}')  
                    self.removeitemclicked = False
                elif success is False:
                    self.messagebox.showmessagebox("Invalid Password", self.WarningLabel.text())
            except Exception:
                self.close()
                
    def to_returned_receipt(self):
        if self.rrecptnum.text() == "":
            self.messagebox.showmessagebox("Empty Customer Number", "Enter Customer Number of Replaced Receipt")
        elif self.rrecptnum.text().isnumeric() is False:
             self.messagebox.showmessagebox("Invalid Customer Number", "Enter Valid Customer Number of Replaced Receipt")
        else:
            try:
                conn = psycopg2.connect(
                    host = "localhost",
                    dbname ='cafe',
                    user = 'postgres',
                    password = '171220',
                    port = 5432)
                cur = conn.cursor()
                
                cuscount = 0
                success = False
                
                cur.execute('SELECT COUNT(RECP_NUM) FROM RECEIPT WHERE CUS_NUM = %s AND RECP_RETURNED = FALSE', (int(self.rrecptnum.text()),))
                for row in cur.fetchone(): 
                    cuscount = int(row)
                
                if cuscount == 0:
                    self.messagebox.showmessagebox("Receipt Cannot Be Returned", "Receipt is Already Returned Previously!\t\t")
                else:
                    recptnum = 0
                    insert_script = 'UPDATE RECEIPT SET RECP_RETURNED = TRUE WHERE CUS_NUM = %s'
                    insert_value = (int(self.rrecptnum.text()),)
                    cur.execute(insert_script, insert_value)
                    
                    cur.execute('SELECT RECP_NUM FROM RECEIPT WHERE CUS_NUM = %s', (int(self.rrecptnum.text()),))
                    for row in cur.fetchone(): 
                        recptnum = int(row)
                    
                    insert_script = 'INSERT INTO RETURNED (RECPT_NUM) VALUES(%s)'
                    insert_value = (int(recptnum),)
                    success = True
                conn.commit()
            except Exception as error:
                self.messagebox.showmessagebox("Returning Receipt Error", "Returning the Receipt is not Successful!\t\t")
            finally:
                if conn is not None:
                    cur.close()
                    conn.close()
                if success:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("Returning the Receipt is Successful!")
                    icon = QIcon()
                    icon.addPixmap(QPixmap("C:\POS SYSTEM2\Finals - final\images\Picsart_23-06-15_09-41-02-215.png"), QIcon.Normal, QIcon.Off)
                    msgBox.setWindowIcon(icon)
                    msgBox.setWindowTitle("Returning Receipt Successful")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.exec()
                
    def show_order(self, id):
        for button in self.menuitemgroup.buttons():
            if button is self.menuitemgroup.button(id):
                self.SelectedOrder.setText(button.text())
                self.prodid = id

    def to_add_order_list(self):
        quantity = self.quantityText.text()
        if(quantity == "" or quantity.isnumeric() is False):
            self.messagebox.showmessagebox("Incorrect Quantity Value", "Input Numbers Only!\t\t")
        elif(self.SelectedOrder.text() == ""):
            self.messagebox.showmessagebox("No Selected Item", "Select Item First!")
        else:
            self.RemoveItemButton.setEnabled(True)
            self.RemoveItemButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            selectedorder = self.SelectedOrder.text().split("\n")
            ordername = selectedorder[0]
            orderprice = selectedorder[1]
            totalorderprice = (float(quantity) * float(orderprice))
            totalorderprice = "{:.2f}".format(totalorderprice)
            spacing = "".rjust(20)
            buttonname = ordername + "\nTotal Price: " + totalorderprice + spacing +"Qty: "+ quantity + "\n"
            self.orderitembutton = QtWidgets.QPushButton(buttonname, self.scrollAreaWidgetContents)
            self.orderitembutton.setMinimumSize(QtCore.QSize(0, 150))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(False)
            font.setWeight(50)
            self.orderitembutton.setFont(font)
            self.orderitembutton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.orderitembutton.setEnabled(False)
            self.orderitembutton.setStyleSheet("background-color: rgb(240, 209, 160, 100%); color: rgb(71, 55, 39, 100%); " + 
                                                  "border-radius: 10px; text-align:left; padding: 20px\n""")
            self.orderitembutton.setObjectName("orderitembutton")
            self.stack.queue_insertion({'Order Name': ordername, 'Quantity': int(quantity), 'Price': float(totalorderprice), 'BtnObject': self.orderitembutton, 'ProdNum': self.prodid})
            self.verticalLayout.addWidget(self.orderitembutton)
            self.orderitemgroup.addButton(self.orderitembutton, self.stack.total_items()) #put id
            self.quantityText.setText("")
            self.SelectedOrder.setText("")
            
    def delete_order(self, id):
        if(self.stack.total_items() == 0):
            self.RemoveItemButton.setEnabled(False)
            self.RemoveItemButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.stackedWidget.setCurrentWidget(self.cashierHome)
        else:
            for button in self.orderitemgroup.buttons():
                if button is  self.orderitemgroup.button(id):  
                    self.stack.delete_item(button)
                    button.deleteLater()
                
    def enable_delete_function(self):
        if self.removeitemclicked: 
            self.removeitemclicked = False  #Clicking Remove item button again
            for button in self.orderitemgroup.buttons():
                button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                button.setEnabled(False)
        else:
            self.removeitemclicked = True #Clicking Remove item button once
            for button in self.orderitemgroup.buttons():
                button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                button.setEnabled(True)
                
    def to_calcu(self):
        if(self.stack.total_items() == 0):
            self.messagebox.showmessagebox("Order Item List Empty", "Select Items to Order First")
        else:
            self.calcu = CashierCalc(self)
            self.calcu.continueClicked.connect(self.handlecontinueClickGenRec)
            self.calcu.set_total_price(self.stack.calcu_total_price())
            self.calcu.exec()
            # Afer Finishing Calcu going Receipt Details
            self.cash = self.calcu.get_cash_received()
            self.customer =  self.calcu.get_customer_name()
            if self.cash != '' and self.customer != '':
                receiptname = "\n"
                customerdetails = "Customer Name: "+ self.customer + "\n\n"
                receiptname = f'{receiptname}{customerdetails}'
                for button in self.orderitemgroup.buttons(): # Accesing Orders Selected
                    receiptname = f'{receiptname}{button.text()}'
                cashdetails = "\nSubtotal: " + str(self.stack.calcu_total_price()) +"\n" + "Total: " + str(self.stack.calcu_total_price()) + "\n\n" + "Received Cash: "+ self.cash +"\n" + "Change: " + str(float(self.cash) - self.stack.calcu_total_price())
                receiptname = f'{receiptname}{cashdetails}'  
                self.ReceiptDetails = QtWidgets.QPushButton(receiptname, self.scrollAreaWidgetContents_2) # Creating the Receipt
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ReceiptDetails.sizePolicy().hasHeightForWidth())
                self.ReceiptDetails.setSizePolicy(sizePolicy)
                self.ReceiptDetails.setMinimumSize(QtCore.QSize(1023, 0))
                font = QtGui.QFont()
                font.setPointSize(12)
                font.setBold(False)
                font.setWeight(50)
                self.ReceiptDetails.setFont(font)
                self.ReceiptDetails.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.ReceiptDetails.setEnabled(False)
                self.ReceiptDetails.setStyleSheet("background-color: rgb(240, 209, 160, 100%); color: rgb(71, 55, 39, 100%); border-radius: 0px; text-align:left; padding: 20px ")
                self.ReceiptDetails.setObjectName("ReceiptDetails")
                self.verticalLayout_2.addWidget(self.ReceiptDetails)
            
    def to_notice_print(self):
        recieptheader = "\nDON MACCHIATOS\nDate: " + self.dateTimeEdit.text() + "\nReceipt #: " + str(self.cntcustomers + 1) + "\nCashier's #: " + str(self.staffid) + "\nCashier's Name: " + self.staffname
        receipt = f'{""""""}{recieptheader}'
        receipt = f'{receipt}{self.ReceiptDetails.text()}' 
        self.record_customer()
        self.record_order()
        self.record_transaction()
        self.record_receipt()
        # self.print_receipt(receipt)
        self.ReceiptDetails.deleteLater()
        for button in self.orderitemgroup.buttons():
            self.stack.delete_item(button)
            button.deleteLater()
        self.addessential_details()
        self.stackedWidget.setCurrentWidget(self.cashierHome)
        
    def to_admin_signin(self):
        self.stackedWidget.setCurrentWidget(self.adminSignIn)

    def to_admin_home(self):
        success = False
        # Sign in
        try:
            with psycopg2.connect(
                    host="localhost",
                    dbname='cafe',
                    user='postgres',
                    password='171220',
                    port=5432) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute('SELECT * FROM ADMINISTRATOR')
                    for record in cur.fetchall():
                        if str(record['adm_num']) == self.AdminEmpNum.text():
                            if str(record['adm_pass']) == self.AdminPass.text():
                                success = True
                                break
                        else:
                            success = False
        except Exception as error:
            self.messagebox.showmessagebox("No Database", "Database is Not Available!")
        finally:
            try:
                if conn is not None:
                    conn.close()
                if success:
                    self.addadmin_details()
                    self.stackedWidget.setCurrentWidget(self.adminHome)
                elif success is False:
                    self.messagebox.showmessagebox("Invalid Password", self.WarningLabel_3.text())
            except Exception:
                self.close()

    def to_edit_product(self):
        self.AddProduct.setEnabled(True)
        self.DeleteProduct.setEnabled(True)
        self.deleteprodid.setEnabled(True)
        self.adminFunction.setCurrentWidget(self.editProduct)

    def to_gen_sales(self):
        self.AddProduct.setEnabled(False)
        self.DeleteProduct.setEnabled(False)
        self.deleteprodid.setEnabled(False)
        self.adminFunction.setCurrentWidget(self.genSalesReport)

    def to_manage_emp(self):
        self.AddProduct.setEnabled(False)
        self.DeleteProduct.setEnabled(False)
        self.deleteprodid.setEnabled(False)
        self.adminFunction.setCurrentWidget(self.manageEmp)
    
    def to_manage_inv(self):
        self.adminFunction.setCurrentWidget(self.manageInv)

    def to_add_product(self):
        self.disable_admin_buttons()
        self.add_product = AddProductAdmin()
        self.add_product.exec()
        self.add_product.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal

    def to_delete_product(self):
        if self.deleteprodid.text() == "":
            self.messagebox.showmessagebox("Empty Product Number\t", "Input Product Number First!")
        else:
            self.AddProduct.setEnabled(False)
            self.DeleteProduct.setEnabled(False)
            self.delete_product = DeleteProductAdmin()
            self.delete_product.exec()
            if self.delete_product.get_confirmed():
                try: 
                    conn = psycopg2.connect(
                        host = "localhost",
                        dbname ='cafe',
                        user = 'postgres',
                        password = '171220',
                        port = 5432)
                    cur = conn.cursor()
                    insert_script = 'UPDATE PRODUCT SET PROD_STAT = 0 WHERE PROD_NUM = %s'
                    insert_value = (int(self.deleteprodid.text()), )
                    cur.execute(insert_script, insert_value)
                    conn.commit()
                except Exception as error:
                    self.messagebox.showmessagebox("Adding Product Error", "Adding New Product is not Successful!\t\t")
                finally:
                    if conn is not None:
                        cur.close()
                        conn.close()
            self.deleteprodid.setText("")
            self.delete_product.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
            self.child_window_closed()  # Connect the closed signal

    def to_edit_productbtn(self):
        self.disable_admin_buttons()
        self.edit_prod = EditProductAdmin()
        self.edit_prod.exec()
        self.edit_prod.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal

    def to_edit_emp(self):
        self.disable_admin_buttons()
        self.AddEmp.setEnabled(False)
        self.edit_emp = EditEmployeeAdmin()
        self.edit_emp.exec()
        self.edit_emp.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal

    def to_add_emp(self):
        self.disable_admin_buttons()
        self.EditEmp.setEnabled(False)
        self.add_emp = AddEmployeeAdmin()
        self.add_emp.exec()
        self.add_emp.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal

    def to_edit_ing(self):
        self.disable_admin_buttons()
        self.edit_ing = EditIngredientsAdmin()
        self.edit_ing.exec()
        self.edit_ing.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal
        
    def to_add_ing(self):
        self.add_ing = AddIngredientsAdmin(self)
        self.add_ing.exec()
        self.add_ing.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.child_window_closed()  # Connect the closed signal

    def disable_admin_buttons(self):
        self.EditProductDetails.setEnabled(False)
        self.AddProduct.setEnabled(False)
        self.DeleteProduct.setEnabled(False)
        self.deleteprodid.setEnabled(False)
        self.adminSO.setEnabled(False)
        self.adminDetails.setEnabled(False)
        self.GenSalesReport.setEnabled(False)
        self.ManageEmp.setEnabled(False)
        self.ManageInv.setEnabled(False)
        
    def child_window_closed(self):
        self.add_product = None
        self.delete_product = None
        self.edit_prod = None
        self.edit_emp = None
        self.add_emp = None
        self.edit_ing = None
        self.calcu = None
        self.to_details = None
        self.to_signout_notice = None
        self.EditProductDetails.setEnabled(True)
        self.AddProduct.setEnabled(True)
        self.DeleteProduct.setEnabled(True)
        self.deleteprodid.setEnabled(True)
        self.adminSO.setEnabled(True)
        self.adminDetails.setEnabled(True)
        self.GenSalesReport.setEnabled(True)
        self.ManageEmp.setEnabled(True)
        self.ManageInv.setEnabled(True)
        self.EditProduct.setEnabled(True)
        self.AddEmp.setEnabled(True)
        self.EditEmp.setEnabled(True)
        self.EditIngredients.setEnabled(True)
        self.addadmin_details()
            
    def to_main(self):
        self.CashierEmpNum.setText(None)
        self.CashierPass.setText(None)
        self.AdminEmpNum.setText(None)
        self.AdminPass.setText(None)
        self.stackedWidget.setCurrentWidget(self.mainSignIn)

    def to_signout_notice(self):
        self.signout_notice = SignOutConfirm(self)
        self.signout_notice.continueClicked.connect(self.handleContinueClicked)
        self.signout_notice.show()
        self.signout_notice.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.signout_notice.closed.connect(self.child_window_closed)  # Connect the closed signal
    
    def handleContinueClicked(self):
        self.stackedWidget.setCurrentWidget(self.mainSignIn)
        self.CashierEmpNum.setText(None)
        self.CashierPass.setText(None)
        self.AdminEmpNum.setText(None)
        self.AdminPass.setText(None)
    
    def handlecontinueClickGenRec(self):
        self.stackedWidget.setCurrentWidget(self.cashierGenReceipt)
        
    def cancelReceipt(self):
        self.ReceiptDetails.deleteLater()
    
    def to_details(self):
        self.details = DetailsDialog(self)
        self.details.show()
        self.details.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Set attribute to delete on close
        self.details.closed.connect(self.child_window_closed)  # Connect the closed signal

    def updateDateTime(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.fromString(current_datetime, "yyyy-MM-dd HH:mm:ss"))
        QtCore.QTimer.singleShot(1000, self.updateDateTime)
        
    def button_clicked(self):
        return True

    def addessential_details(self):
        # Fetching products
        try:
            with psycopg2.connect(
                    host='localhost',
                    dbname='cafe',
                    user='postgres',
                    password='171220',
                    port=5432) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute('SELECT PROD_NUM, PROD_NAME, PROD_PRICE FROM PRODUCT WHERE PROD_STAT = 1')
                    for record in cur.fetchall():
                        productnum = int(record['prod_num'])
                        button_name = str(record['prod_name']) + "\n" + str(record['prod_price'])
                        self.create_menubuttons(button_name, productnum)
                        if record is None:
                            self.messagebox.showmessagebox("No Records", "No Products fround. Please Insert first.")

                    cur.execute('SELECT COUNT(ORDER_NUM) FROM CUS_ORDER')
                    for record in cur.fetchall():
                        self.cntorders = int(record['count'])
                        orders = str(record['count'])
                        maxorder = "Maximum Number of \nOrders:\n\n"
                        totalcustomer = "Total Customers \nServed Today:\n\n"
                        self.MaxOrder.setText(f'{maxorder}{orders}')
                        
                    cur.execute('SELECT COUNT(CUS_NUM) FROM CUSTOMER WHERE CUS_CREATED_AT = CURRENT_DATE')
                    for record in cur.fetchall():
                        customerstdy = int(record['count'])
                        totalcustomer = "Total Customers \nServed Today:\n\n"
                        self.TotalCustomers.setText(f'{totalcustomer}{str(customerstdy)}')
                        
                    cur.execute('SELECT SUM(TRANS_PRICE) FROM CUS_TRANSACTION WHERE TRANS_CREATED_AT = CURRENT_DATE')
                    for record in cur.fetchall():
                        sales = str(record['sum'])
                        totalsales = "Total Sale/s for \nToday:\n\n"
                        self.TotalSales.setText(f'{totalsales}{sales}')
                        
                    cur.execute('SELECT COUNT(CUS_NUM) FROM CUSTOMER')
                    for record in cur.fetchall():
                        self.cntcustomers = int(record['count'])
                        
                    cur.execute('SELECT COUNT(TRANS_NUM) FROM CUS_TRANSACTION WHERE TRANS_CREATED_AT = CURRENT_DATE')
                    for record in cur.fetchall():
                        self.alltransnum = int(record['count'])
                        totaltransactions= "Total Transactions Made \nToday:\n\n"
                        self.TotalTransactions.setText(f'{totaltransactions}{str(self.alltransnum)}')
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    def create_menubuttons(self, button_name, col):
        self.button = QtWidgets.QPushButton(button_name, self.menuItemScroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.button.setFont(font)
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button.setStyleSheet("background-color: rgb(240, 209, 160, 100%); border-radius: 10px; padding: 20px; margin: 0px 2.5px; color: rgb(71, 55, 39, 100%);")
        self.button.setObjectName("MenuItem1")
        self.gridLayout_3.addWidget(self.button, 0, col, 1, 1)
        self.menuitemgroup.addButton(self.button, col)
        
    def record_customer(self):
          # Recording orders
        try:
            conn = psycopg2.connect(
                host = "localhost",
                dbname ='cafe',
                user = 'postgres',
                password = '171220',
                port = 5432)
            cur = conn.cursor()
            insertcus_script = 'INSERT INTO CUSTOMER (CUS_NAME) VALUES (%s)'
            insertcus_value = (self.customer,)
            cur.execute(insertcus_script, insertcus_value)
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
    def record_order(self):
        try:
            conn = psycopg2.connect(
                host = "localhost",
                dbname ='cafe',
                user = 'postgres',
                password = '171220',
                port = 5432)
            cur = conn.cursor()
            insertorder_script  = 'INSERT INTO CUS_ORDER (CUS_NUM, STAFF_NUM, ORDER_NAME) VALUES (%s, %s, %s)'
            insertorder_values  = (self.cntcustomers + 1, self.staffid, 'Regular')
            cur.execute(insertorder_script, insertorder_values)
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
    def record_transaction(self):
        try:
            conn = psycopg2.connect(
                host = "localhost",
                dbname ='cafe',
                user = 'postgres',
                password = '171220',
                port = 5432)
            cur = conn.cursor()
            inserttrans_script  = 'INSERT INTO CUS_TRANSACTION(TRANS_QUANT, TRANS_PRICE, ORDER_NUM, PROD_NUM) VALUES (%s, %s, %s, %s)'
            inserttrans_values  = []
            for seqnum in range(1, self.stack.total_items()+1):
                orderqnt = self.stack.get_order_quant(seqnum)
                orderprice = self.stack.get_order_price(seqnum)
                prodnum = self.stack.get_prod_num(seqnum)
                cusorder = (orderqnt, orderprice, self.cntorders+1, prodnum)
                inserttrans_values.append(cusorder)
            for record in inserttrans_values:
                cur.execute(inserttrans_script, record)
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
                
    def record_receipt(self):
        try:
            conn = psycopg2.connect(
                host = "localhost",
                dbname ='cafe',
                user = 'postgres',
                password = '171220',
                port = 5432)
            cur = conn.cursor()
            insertrcpt_script  = 'INSERT INTO RECEIPT(STAFF_NUM, CUS_NUM, TRANS_NUM) VALUES (%s, %s, %s)'
            insertrcpt_values  = []
            for seqnum in range(1, self.stack.total_items()+1):
                rcpt = (self.staffid, self.cntcustomers + 1, self.alltransnum + seqnum)
                insertrcpt_values.append(rcpt)
            for record in insertrcpt_values:
                cur.execute(insertrcpt_script, record)   
            conn.commit()

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
     
    def print_receipt(self, text):
        # Get the default printer name
        printer_name = win32print.GetDefaultPrinter()
        # Open a handle to the printer
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            # Start a new print job
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Receipt", None, "RAW"))
            try:
                # Start a new page within the print job
                win32print.StartPagePrinter(hPrinter)

                # Write the receipt text to the printer
                win32print.WritePrinter(hPrinter, text.encode('utf-8'))
                
                # Send a form feed command to eject the paper
                win32print.WritePrinter(hPrinter, b'\x0C')

                # End the current page
                win32print.EndPagePrinter(hPrinter)
            finally:
                # End the print job
                win32print.EndDocPrinter(hPrinter)
        finally:
            # Close the printer handle
            win32print.ClosePrinter(hPrinter)
            
    def addadmin_details(self):
        # Fetching products
        try:
            with psycopg2.connect(
                    host='localhost',
                    dbname='cafe',
                    user='postgres',
                    password='171220',
                    port=5432) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute('SELECT PROD_NUM, PROD_NAME, PROD_PRICE FROM PRODUCT WHERE PROD_STAT = 1')
                    for record in cur.fetchall():
                        productcount = int(record['prod_num'])
                        product_name = "Product Num: " + str(record['prod_num']) + "\t\t\t\t" + str(record['prod_name']) + "\t\t\t\t" + str(record['prod_price'])
                        self.add_products_to_admin(product_name, productcount)
                        if record is None:
                            self.messagebox.showmessagebox("No Records", "No Products fround. Please Insert first.")
                    
                    cur.execute('SELECT * FROM STAFF')
                    for record in cur.fetchall():
                        staffcount = int(record['staff_num'])
                        stafflname = str(record['staff_lname'])
                        stafffname = str(record['staff_fname'])
                        staffiscas = str(record['staff_is_cas'])
                        self.add_staff_to_admin(stafflname, stafffname, staffiscas, staffcount)
                        if record is None:
                            self.messagebox.showmessagebox("No Records", "No Products fround. Please Insert first.")
                            
                    cur.execute('SELECT * FROM INGREDIENT')
                    for record in cur.fetchall():
                        ingnum = int(record['ingred_num'])
                        ingname = str(record['ingred_name'])
                        ingquant = str(record['ingred_quant']) + " " + str(record['ingred_unit'])
                        ingused = str(record['ingred_used'])
                        self.add_ingred_to_admin(ingnum, ingname, ingquant, ingused)
                        if record is None:
                            self.messagebox.showmessagebox("No Records", "No Products fround. Please Insert first.")
                            
                    cur.execute('SELECT COUNT(TRANS_NUM), SUM(TRANS_PRICE), SUM(TRANS_QUANT) AS "TOTAL PRODUCTS SOLD" FROM CUS_TRANSACTION')
                    for record in cur.fetchall():
                        sales = int(record['sum'])
                        totalproducts = int(record['TOTAL PRODUCTS SOLD'])
                        ordersmade = int(record['count'])
                        self.totalOrderMade.setText(str(ordersmade))
                        self.totalSales.setText(str(sales))
                        self.totalProdSold.setText(str(totalproducts))
                        
                    cur.execute('SELECT AVG(CUS_TRANSACTION.TRANS_QUANT)::numeric(10,2) AS "AVERAGE NUMBER OF PRODUCTS SOLD PER DAY", ' + 
                                'AVG(CUS_ORDER.CUS_NUM)::numeric(10,2) AS "AVERAGE CUSTOMERS SERVED PER DAY",' + 
                                'AVG(CUS_TRANSACTION.TRANS_NUM)::numeric(10,2) AS "AVERAGE NUMBER OF ORDERS MADE PER DAY" ' + 
                                'FROM CUS_ORDER INNER JOIN CUS_TRANSACTION USING(ORDER_NUM)')
                    for record in cur.fetchall():
                        avgprod = str(record['AVERAGE NUMBER OF PRODUCTS SOLD PER DAY'])
                        avgcust = str(record['AVERAGE CUSTOMERS SERVED PER DAY'])
                        avgordr = str(record['AVERAGE NUMBER OF ORDERS MADE PER DAY'])
                        self.avgProdSoldperday.setText(avgprod)
                        self.avgCusServedperday.setText(avgcust)
                        self.avgOrdersperday.setText(avgordr)
                        
                    cur.execute('SELECT COUNT(CUS_NUM) FROM CUSTOMER')
                    for record in cur.fetchall():
                        customers = str(record['count'])
                        self.totalCusServed.setText(customers)
                        
                    cur.execute('SELECT COUNT(RTND_NUM) FROM RETURNED')
                    for record in cur.fetchall():
                        returned = str(record['count'])
                        self.totalReturns.setText(returned)
                            
                    
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def add_products_to_admin(self, productname, prodcount):
        self.product_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_label.sizePolicy().hasHeightForWidth())
        self.product_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.product_label.setFont(font)
        self.product_label.setStyleSheet("background-color: rgb(214, 156, 114, 100%); color: rgb(71, 55, 39, 100%); border-radius: 10px; padding: 40px 0px;")
        self.product_label.setAlignment(QtCore.Qt.AlignCenter)
        self.product_label.setObjectName("product" + str(prodcount))
        self.product_label.setText(productname)
        self.gridLayout.addWidget(self.product_label, prodcount, 1, 1, 1)

    def add_staff_to_admin(self, stafflname, stafffname, staffcas, staffcount):
        self.num = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.num.sizePolicy().hasHeightForWidth())
        self.num.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.num.setFont(font)
        self.num.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.num.setAlignment(QtCore.Qt.AlignCenter)
        self.num.setObjectName("num" + str(staffcount))
        self.num.setText(str(staffcount))
        self.gridLayout_2.addWidget(self.num, staffcount, 0, 1, 1)
        
        self.lname = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lname.sizePolicy().hasHeightForWidth())
        self.lname.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lname.setFont(font)
        self.lname.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.lname.setAlignment(QtCore.Qt.AlignCenter)
        self.lname.setObjectName("lname" + str(staffcount))
        self.lname.setText(stafflname)
        self.gridLayout_2.addWidget(self.lname, staffcount, 1, 1, 1)
        
        self.fname = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fname.sizePolicy().hasHeightForWidth())
        self.fname.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.fname.setFont(font)
        self.fname.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.fname.setAlignment(QtCore.Qt.AlignCenter)
        self.lname.setObjectName("fname" + str(staffcount))
        self.fname.setText(stafffname)
        self.gridLayout_2.addWidget(self.fname, staffcount, 2, 1, 1)
        
        self.staffiscas = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffiscas.sizePolicy().hasHeightForWidth())
        self.staffiscas.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.staffiscas.setFont(font)
        self.staffiscas.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.staffiscas.setAlignment(QtCore.Qt.AlignCenter)
        self.staffiscas.setObjectName("staffiscas" + str(staffcount))
        self.staffiscas.setText(staffcas)
        self.gridLayout_2.addWidget(self.staffiscas, staffcount, 3, 1, 1)

    def add_ingred_to_admin(self, ingnum, ingname, ingquant, ingused):
        self.ing_num = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ing_num.sizePolicy().hasHeightForWidth())
        self.ing_num.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ing_num.setFont(font)
        self.ing_num.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.ing_num.setAlignment(QtCore.Qt.AlignCenter)
        self.ing_num.setObjectName("ingnum" + str(ingnum))
        self.ing_num.setText(str(ingnum))
        self.gridLayout_4.addWidget(self.ing_num, ingnum, 0, 1, 1)
        
        self.ing_name = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ing_name.sizePolicy().hasHeightForWidth())
        self.ing_name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ing_name.setFont(font)
        self.ing_name.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.ing_name.setAlignment(QtCore.Qt.AlignCenter)
        self.ing_name.setObjectName("ingname" + str(ingnum))
        self.ing_name.setText(str(ingname))
        self.gridLayout_4.addWidget(self.ing_name, ingnum, 1, 1, 1)
        
        self.ing_quant = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ing_quant.sizePolicy().hasHeightForWidth())
        self.ing_quant.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ing_quant.setFont(font)
        self.ing_quant.setStyleSheet("background-color: white; color: rgb(71, 55, 39, 100%); border-radius: 5px; padding: 10px 0px;")
        self.ing_quant.setAlignment(QtCore.Qt.AlignCenter)
        self.ing_quant.setObjectName("ingquant" + str(ingnum))
        self.ing_quant.setText(str(ingquant))
        self.gridLayout_4.addWidget(self.ing_quant, ingnum, 2, 1, 1)
        
        
        
def main():
    app = QApplication([])
    window = MainWindow()
    app.exec_()

if __name__ == '__main__':
    main()
