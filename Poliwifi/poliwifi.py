import poliwifi
from PyQt4.QtGui import QApplication
from sys import argv

if __name__ == "__main__":
    app=QApplication(argv)
    test = org.poul.poliwifi.PoliWifi()
    test.show()
    app.exec_()
    
    