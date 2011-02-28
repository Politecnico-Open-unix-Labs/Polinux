# This file is part of the Polinux project.
#
# Copyright(c) 2011 Radu Andries
# http://www.poul.org/
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import interface
import nm
from PySide import QtGui
from PySide.QtCore import QObject,SIGNAL,SLOT
from gui import Wizard
import networkmanager
import networkmanager.applet.settings as settings

class PoliWifiLinux(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.window = Wizard()
        self.handler = interface.Ui_poliwifi()
        self.handler.setupUi(self.window)
        self.window.setOption(QtGui.QWizard.NoBackButtonOnStartPage,True)
        self.openssid="polimi"
        self.openconn=None
        
    def show(self):
        self.handler.polimi_status.setVisible(False)
        self.handler.polimi_statusbar.setVisible(False)
        self.nmhandler=nm.NetworkManagerClient()
        self.openap=None
        if self.nmhandler.wireless!=None:
            self.openap=self.nmhandler.findAPbyName(self.openssid) #TODO
        if not self.openap:
            self.window.goto_finish=True
            self.handler.aperror.setText(self.tr("<b><font color='red'>Polimi AP is not in range. Are you under wifi coverage?<b></font>"))
            self.handler.aperror.setVisible(True)
        QObject.connect(self.window,SIGNAL("currentIdChanged(int)"),self,SLOT("pageChanged(int)"))
        self.window.show()
    def pageChanged(self,id):
        if id==1:
            self.handler.polimi_status.setVisible(True)
            self.handler.polimi_statusbar.setVisible(True)
            self.window.button(Wizard.NextButton).setVisible(False)
            self.window.button(Wizard.BackButton).setVisible(False)
            self.nmhandler.nm._connect_to_signal("StateChanged", self.connectionStateChanged)
            self.connectToOpenAp()
            
    def connectToOpenAp(self):
        for conn in self.nmhandler.applet.ListConnections():
            cs=conn.GetSettings()
            if ("802-11-wireless" in cs) and cs["802-11-wireless"]["ssid"]=="polimi":
                self.openconn=cs
        if not self.openconn:
            c=settings.WiFi(self.openssid)
            self.nmhandler.applet.AddConnection(c.ConMap())
        self.nmhandler.connectTo(self.openssid)
        
    def connectionStateChanged(self,status):
        status1=networkmanager.NetworkManager.State(3)
        if str(status)==str(status1):
            self.handler.polimi_status.setText(self.tr("<b><font color='green'>Connection established</font></b>"))
            self.handler.polimi_statusbar.setVisible(False)
            self.window.button(Wizard.NextButton).setVisible(True)