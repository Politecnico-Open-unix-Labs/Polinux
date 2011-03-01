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
from networkmanager.applet import SYSTEM_SERVICE
from workers import Runner
from mechanize import Browser


class PoliWifiLinux(QObject):
    '''Base class'''
    def __init__(self):
        QObject.__init__(self)
        self.window = Wizard()
        self.handler = interface.Ui_poliwifi()
        self.handler.setupUi(self.window)
        self.window.setOption(QtGui.QWizard.NoBackButtonOnStartPage,True)
        self.openssid="polimi"
        self.openconn=None
        self.polimiconnected=False
        self.auth=None
        self.downloader=None
        self.browser=None
    def show(self):
        '''Shows GUI. Initializes NM'''
        self.handler.polimi_status.setVisible(False)
        self.handler.polimi_statusbar.setVisible(False)
        self.nmhandler=nm.NetworkManagerClient()
        if self.nmhandler.wireless["state"]==8:
            self.nmhandler.wireless.Disconnect()
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
        '''Called when page in the Wizard is changed'''
        self.handler.polimi_statusbar.setVisible(False)
        if id==1 and not self.polimiconnected:
            self.handler.polimi_status.setVisible(True)
            self.handler.polimi_statusbar.setVisible(True)
            self.window.button(Wizard.NextButton).setVisible(False)
            self.window.button(Wizard.BackButton).setVisible(False)
            self.connectToOpenAp()
        elif id==3:
            self.window.button(Wizard.NextButton).setVisible(False)
            self.window.button(Wizard.BackButton).setVisible(False)
            self.workersStart()
            
    def connectToOpenAp(self):
        '''Connects to "polimi"'''
        for conn in self.nmhandler.applet.ListConnections():
            cs=conn.GetSettings()
            if ("802-11-wireless" in cs) and cs["802-11-wireless"]["ssid"]=="polimi":
                self.openconn=cs
        if not self.openconn:
            c=settings.WiFi(self.openssid)
            self.nmhandler.applet.AddConnection(c.ConMap())
            self.nmhandler.applet.connect_to_signal("NewConnection", self.connectToOpenAp_helper,"org.freedesktop.NetworkManagerSettings")
        else:
            self.connectToOpenAp_helper()
    def connectToOpenAp_helper(self,*args,**kwargs):
        '''Helper function'''
        if not self.nmhandler.connectTo(self.openssid):
            self.handler.polimi_status.setText(self.tr("<b><font color='red'>Cannot connect to Polimi AP<b></font>"))
            self.handler.polimi_statusbar.setVisible(False)
            self.window.goto_finish=True
        self.nmhandler.wireless.connect_to_signal("StateChanged", self.connectionStateChanged,"org.freedesktop.NetworkManager.Device")
            
    def connectionStateChanged(self,newstate,oldstate,reason):
        '''When connection changes'''
        if newstate==8:
            self.handler.polimi_status.setText(self.tr("<b><font color='green'>Connection established</font></b>"))
            self.handler.polimi_statusbar.setVisible(False)
            self.window.button(Wizard.NextButton).setVisible(True)
            self.polimiconnected=True
    def workersStart(self):
        self.browser=Browser()
        
        anonuser = {
                  0: lambda m: "S"+m,
                  1: lambda m: "D"+m,
                  2: lambda m: "U"+m,
                  3: lambda m: "V"+m
        }[self.handler.usertype.currentIndex()](self.handler.matricola.text())
        self.auth=Runner(self.nmhandler,self.handler.personCode.text(), self.handler.personCodePwd.text(),anonuser,self.handler.certificatepassword.text(),self.handler.progress_status,self.handler.progress_statusbar)
        self.connect(self.auth,SIGNAL("finished()"),self,SLOT("downloadDone()"))
        self.connect(self.auth,SIGNAL("statusChanged(int,QString)"),self,SLOT("updateProgress(int,QString)"))
        self.auth.start()
    def downloadDone(self):
        self.window.button(Wizard.NextButton).setVisible(True)
    def updateProgress(self,num,text):
        self.handler.progress_status.setText(text)
        self.handler.progress_statusbar.setValue(num)