from poliwifi import PoliWifiLinux,nm
from PyQt4.QtGui import QApplication
from sys import argv

if __name__ == "__main__":
    app=QApplication(argv)
    test = PoliWifiLinux()
    test.show()
    app.exec_()
    
    