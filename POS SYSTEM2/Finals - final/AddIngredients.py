from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, uic
from messagebox import Message
import psycopg2
import psycopg2.extras

class AddIngredientsAdmin(QDialog): 
    closed = QtCore.pyqtSignal()  # Custom signal for child window closed
 
    def __init__(self, parent=None):
        super(AddIngredientsAdmin, self).__init__(parent)
        uic.loadUi(r"C:\POS SYSTEM2\Finals - final\ui\AddIngredients.ui", self)
        self.show()
 
        self.messagebox = Message()
        
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        width = 800
        height = 455
        self.resize(width, height)
        self.setFixedSize(width, height)
        self.Cancel.clicked.connect(self.exit_edit)
        self.Add.clicked.connect(self.add_ing)

    def exit_edit(self):
        self.close()

    def add_ing(self):
        # add logic to add ingredients to table
        if self.NewIngName.text() == "" or self.NewIngQuant.text() == "":
            self.messagebox.showmessagebox("Incomplete Form", "Input Needed Ingredients Details First!")
        else:
            try:
                ingredientquunit = self.NewIngQuant.text().split(',')
                self.Ingredientquant = int(ingredientquunit[0])
                self.Ingredientunit = ingredientquunit[1]
                try:
                    tryconvert = float(self.Ingredientunit)
                    self.messagebox.showmessagebox("Ingredient Unit Invalid", "Input Ingredient Unit in Abbriviated Form!\t")
                except Exception as error:
                    if(self.Ingredientquant < 0):
                        self.messagebox.showmessagebox("Negative Ingredient Quantity Inputted", "Input Valid Ingredient Quantity Only!\t")
                    elif len(self.Ingredientunit) > 20:
                        self.messagebox.showmessagebox("Ingredient Unit Not Abbriviated", "Input Ingredient Unit in Abbriviated Form!\t")
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
                            insert_script = 'INSERT INTO INGREDIENT(INGRED_NAME, INGRED_QUANT, INGRED_UNIT) VALUES(%s, %s, %s)'
                            insert_value = (self.NewIngName.text(), self.Ingredientquant, self.Ingredientunit.strip())
                            cur.execute(insert_script, insert_value)
                            conn.commit()
                        except Exception as error:
                            self.messagebox.showmessagebox("Adding Ingredient Error", "Adding New Ingredient is not Successful!")
                        finally:
                            if conn is not None:
                                cur.close()
                                conn.close()
                                self.close()
            except Exception as error:
                self.messagebox.showmessagebox("Incorrect Ingredient Quantity Value", "Input Numbers Only!")
        self.close()

    def closeEvent(self, event):
        self.closed.emit()  # Emit the closed signal
        event.accept()


def main():
    app = QApplication([])
    window = AddIngredientsAdmin()
    app.exec()

if __name__ == '__main__':
    main()












