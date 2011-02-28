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

START_URL = "https://www.asi.polimi.it/rete/wifi/richiesta_certificato.html"
DOWNLOAD_URL = "http://www.asi.polimi.it/util/download.html?type=certificato"
CERT_LOCATION = "~/.poli/CertificatoASI.p12"
FOLDER_MODE = 0700
PROXY = "proxy.polimi.it:8080"

class Authenticator(QThread):
    '''
    Authenticates to polimi
    '''

    def __init__(self,user,password):
        '''
        Constructor
        '''
        QThread.__init__(self)
        self.triumph = True
        self.user = user
        self.password = password
        self.bro = Browser()
        if PROXY:
            self.bro.set_proxies({"http":PROXY,"https":PROXY})
        self.bro.set_handle_robots(0)
    
    def run(self):
        self.bro.open(START_URL)
        self.bro.follow_link(text='logon')
        self.bro.select_form('')
        self.bro.form['login'] = self.user
        self.bro.form['password'] = self.password
        self.bro.submit()
        response = self.bro.open(START_URL)

class Downloader(QThread):
    '''
    Downloads the certificate file
    '''

    def __init__(self,browser, passphrase):
        QThread.__init__(self)
        self.bro = browser
        self.passphrase = passphrase
        self.certLocation = os.path.expanduser(CERT_LOCATION) # os.path etc.. Serve per trasformare ~ in /home/$utente
        self.certFolder = os.path.split(self.certLocation)    # Ricava il path solo della cartella
    
    def run(self):
        self.response = self.bro.open(START_URL)
        self.response = self.bro.follow_link(text='nuovo certificato')
        self.bro.select_form(name='exists')
        self.bro.submit()
        
        self.bro.select_form(name='passphrase')
        self.bro.form['passphrase'] = self.passphrase
        self.bro.form['passphraseCheck'] = self.passphrase
        tempfile = self.bro.retrieve(bro.form.click('_qf_passphrase_next'))
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
        













