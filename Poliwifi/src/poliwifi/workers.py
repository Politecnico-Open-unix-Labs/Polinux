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
import re

START_URL="https://www.asi.polimi.it/rete/wifi/richiesta_certificato.html"
PROXY="proxy.polimi.it:8080"
class Authenticator(QThread):
    '''
    Authenticates to polimi
    '''
    def __init__(self,user,password):
        '''
        Constructor
        '''
        QThread.__init__(self)
        self.triumph=True
        self.user=user
        self.password=password
        self.bro=Browser()
        if PROXY:
            self.bro.set_proxies({"http":PROXY,"https":PROXY})
        self.bro.set_handle_robots(0)
    def run(self):
        self.bro.open(START_URL)
        self.bro.follow_link(text='logon')
        self.bro.select_form('')
        self.bro.form['login']=self.user
        self.bro.form['password']=self.password
        self.bro.submit()
        response=self.bro.open(START_URL)
        