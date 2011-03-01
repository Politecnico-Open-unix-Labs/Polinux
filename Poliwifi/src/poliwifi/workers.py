# This file is part of the Polinux project.
#
# Copyright(c) 2011 Radu Andries
# Copyright(c) 2011 Daniele Iamartino
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
from PySide.QtCore import QThread,Signal
from mechanize import Browser
import os
from subprocess import Popen,PIPE
import networkmanager.applet.settings as settings

START_URL = "https://www.asict.polimi.it/rete/wifi/richiesta_certificato.html"
DOWNLOAD_URL = "https://www.asict.polimi.it/util/download.html?type=certificato"
CERT_LOCATION = "~/.poli/CertificatoASI.p12"
FOLDER_MODE = 0700
PROXY = "proxy.polimi.it:8080"
CMD_OSSL="openssl pkcs12 -cacerts -in {0} -out {1} -passin stdin -passout stdin"
CLOSED_AP="internet"

class Runner(QThread):
    '''
    Authenticates to polimi and downloads cert
    '''
    statusChanged = Signal(int,unicode)
    def __init__(self,nm,user,password,anonuser,certPass,ptext,pbar):
        '''
        Constructor
        '''
        QThread.__init__(self)
        self.triumph = True
        self.user = user
        self.nm_iface=nm.applet
        self.anonuser = anonuser
        self.password = password
        self.passphrase=certPass
        self.certLocation=os.path.expanduser(CERT_LOCATION)
        self.certFolder=os.path.split(self.certLocation)[0]
        self.bro = Browser()
        if PROXY:
            self.bro.set_proxies({"http":PROXY,"https":PROXY})
        self.bro.set_handle_robots(0)
    def run(self):
        self.statusChanged.emit(0,self.tr("Connecting to ASICT..."))
        self.bro.open(START_URL)
        self.bro.follow_link(text='logon')
        self.statusChanged.emit(15,self.tr("Logging in..."))
        self.bro.select_form('')
        self.bro.form['login'] = str(self.user)
        self.bro.form['password'] = str(self.password)
        self.bro.submit()
        self.response = self.bro.open(START_URL)
        self.statusChanged.emit(40,self.tr("Downloading certificate.."))
        self.response = self.bro.follow_link(text='nuovo certificato')
        self.bro.select_form(name='exists')
        self.bro.submit()
        self.bro.select_form(name='passphrase')
        self.bro.form['passphrase'] = self.passphrase
        self.bro.form['passphraseCheck'] = self.passphrase
        tempfile = self.bro.retrieve(self.bro.form.click('_qf_passphrase_next'))
        response = self.bro.open(DOWNLOAD_URL)
        del tempfile
        if not os.path.exists(self.certFolder):
            os.mkdir(self.certFolder, FOLDER_MODE) # Non c'e'? La creo! Permessi di default 0700
        try:
            f = open(self.certLocation, "w") 
            f.write(response.read())
            f.close()
        except IOError:
            print "I/O Error during file writing"
        self.statusChanged.emit(70,self.tr("Creating CA certificate..."))
        popen_obj=Popen(CMD_OSSL.format(self.certLocation,os.path.join(self.certFolder,"asi.cer")), shell=True,stdin=PIPE,stdout=PIPE)
        popen_obj.communicate(self.passphrase+"\n"+self.passphrase)
        self.statusChanged.emit(90,self.tr("Creating NM connection..."))
        c=settings.WiFi(CLOSED_AP)
        c["802-11-wireless"]["security"]="802-11-wireless-security"
        c["802-11-wireless-security"]={}
        c["802-11-wireless-security"]["key-mgmt"]="wpa-eap"
        c["802-11-wireless-security"]["auth-alg"]="open"
        c["802-1x"]={}
        c["802-1x"]["eap"]=['tls']
        c["802-1x"]["anonymous-identity"]= self.anonuser
        c["802-1x"]["ca-cert"]="file://"+os.path.join(self.certFolder,"asi.cer")+"\0"
        c["802-1x"]["private-key"]="file://"+self.certLocation+"\0"
        c["802-1x"]["private-key-password"]=self.passphrase
        c["802-1x"]["phase2-auth"]="mschapv2"
        self.nm_iface.AddConnection(c.conmap)
        self.statusChanged.emit(100,self.tr("Done"))










