import org.poul.interface
from PyQt4 import QtGui


class PoliWifi:
    def __init__(self):
        self.window = QtGui.QWizard()
        self.handler = org.poul.interface.Ui_poliwifi()
        self.handler.setupUi(self.window)
    def show(self):
        self.handler.polimi_status.setVisible(False)
        self.handler.polimi_statusbar.setVisible(False)
        self.window.show()