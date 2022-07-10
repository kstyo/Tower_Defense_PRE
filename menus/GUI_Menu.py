from Qt_GUI.Menu_Principal import *
from Qt_GUI.Menu_Nueva_Partida import *
from Qt_GUI.Menu_Ajustes import *

import sys

class GUI_Menu (Ui_MainWindow):
    def __init__ (self, window):
        
    def clickMe(self):

    def showName(self):



app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = GUI_Menu(MainWindow)
#ui.setupUi(MainWindow)
MainWindow.show()
app.exec_()
