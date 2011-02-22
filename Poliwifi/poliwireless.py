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

from poliwifi import PoliWifiLinux,nm
from PyQt4.QtGui import QApplication
from sys import argv
import subprocess
import os

if __name__ == "__main__":
    #if os.getuid()!=0:
    #    subprocess.call(["gksudo", "--description", "poliwifi","python "+__file__])
    #else:
        app=QApplication(argv)
        gui = PoliWifiLinux()
        gui.show()
        app.exec_()
    
    