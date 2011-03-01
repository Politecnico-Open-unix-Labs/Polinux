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
from PySide.QtCore import QThread
from mechanize import Browser
import os
from subprocess import Popen,PIPE

START_URL = "https://www.asict.polimi.it/rete/wifi/richiesta_certificato.html"
DOWNLOAD_URL = "https://www.asict.polimi.it/util/download.html?type=certificato"
CERT_LOCATION = "~/.poli/CertificatoASI.p12"
FOLDER_MODE = 0700
PROXY = "proxy.polimi.it:8080"
CMD_OSSL="openssl pkcs12 -cacerts -in {0} -out {1} -passin stdin -passout stdin"

class Runner(QThread):
    '''
    Authenticates to polimi and downloads cert
    '''

    def __init__(self,user,password,anonuser,certPass,ptext,pbar):
        '''
        Constructor
        '''
        QThread.__init__(self)
        self.triumph = True
        self.user = user
        #self.pbar = pbar
        #self.ptext=ptext
        self.password = password
        self.passphrase=certPass
        self.certLocation=os.path.expanduser(CERT_LOCATION)
        self.certFolder=os.path.split(self.certLocation)[0]
        self.bro = Browser()
        if PROXY:
            self.bro.set_proxies({"http":PROXY,"https":PROXY})
        self.bro.set_handle_robots(0)
        #self.pbar.setValue(0)
    def run(self):
        #self.ptext.setText(self.tr("Connecting to ASICT..."))
        self.bro.open(START_URL)
        self.bro.follow_link(text='logon')
        #self.pbar.setValue(15)
        #self.ptext.setText(self.tr("Logging in..."))
        self.bro.select_form('')
        self.bro.form['login'] = str(self.user)
        self.bro.form['password'] = str(self.password)
        self.bro.submit()
        self.response = self.bro.open(START_URL)
        #self.pbar.setValue(40)
        #self.ptext.setText(self.tr("Downloading certificate.."))
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
        #self.pbar.setValue(70)
        #self.ptext.setText(self.tr("Creating CA certificate..."))
        popen_obj=Popen(CMD_OSSL.format(self.certLocation,os.path.join(self.certFolder,"asi.cer")), shell=True,stdin=PIPE,stdout=PIPE)
        popen_obj.communicate(self.passphrase+"\n"+self.passphrase)
        #self.pbar.setValue(90)
        #self.ptext.setText(self.tr("Creating NM connection..."))











