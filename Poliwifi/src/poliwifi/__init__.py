import interface
import nm
from PyQt4 import QtGui


class PoliWifiLinux:
    def __init__(self):
        self.window = QtGui.QWizard()
        self.handler = interface.Ui_poliwifi()
        self.handler.setupUi(self.window)
    def show(self):
        self.handler.polimi_status.setVisible(False)
        self.handler.polimi_statusbar.setVisible(False)
        nmhandler=nm.NetworkManager()
        print nmhandler.findAPbyName("polimi")
        self.window.show()