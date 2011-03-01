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

import networkmanager
from networkmanager.applet import NetworkManagerSettings, USER_SERVICE, SYSTEM_SERVICE

import dbus
from dbus.mainloop.qt import DBusQtMainLoop
class NetworkManagerClient(object):
    '''
    Handles connection of networkmanager
    '''


    def __init__(self):
        '''
        Constructor
        '''
        dbus.set_default_main_loop(DBusQtMainLoop())
        self.nm=networkmanager.NetworkManager()
        devices=self.nm.GetDevices()
        self.wireless = None
        self.ap=None
        self.success = True
        witype=networkmanager.device.Device.DeviceType(2)
        for device in devices:
            if str(device["DeviceType"])==str(witype):
                self.wireless=device
                break
        if self.wireless == None:
            print "No Devices Found"
            self.success = False
        self.applet=NetworkManagerSettings(SYSTEM_SERVICE)

                    
    def connectTo(self,ssid):
        '''Connects to wireless AP.
            >>Implies that connection exists
            @return: returns False if connection doesn't exist
        '''
        connected=False
        self.applet=NetworkManagerSettings(SYSTEM_SERVICE)
        for conn in self.applet.ListConnections():
            cs=conn.GetSettings()
            if ("802-11-wireless" in cs) and cs["802-11-wireless"]["ssid"]==ssid:
                self.nm.ActivateConnection(SYSTEM_SERVICE,conn.object_path,self.wireless.object_path,"/")
                connected=True
        if connected:
            return True
        return False
    
    def findAPbyName(self,ssid):
        '''Finds AP object by name. Returns only AP with most strength
            @return: The DBUS Object representing the IP
        '''
        maxpower=0
        maxap=None
        for ap in self.wireless.GetAccessPoints():
            if ap["Strength"]>maxpower and ap["Ssid"]==ssid :
                maxap=ap
                maxpower=ap["Strength"]
        return maxap
    
    def getConnectionByName(self):
        '''STUB'''
        pass