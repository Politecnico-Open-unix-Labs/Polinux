'''
Created on 22/feb/2011

@author: admiral0
'''
import dbus
#from dbus.mainloop.glib import DBusGMainLoop
from dbus.mainloop import qt
class NetworkManager(object):
    '''
    Handles connection of networkmanager
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.bus=dbus.SystemBus(mainloop=qt.DBusQtMainLoop(set_as_default=True))
        nmproxy=self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        self.nm=dbus.Interface(nmproxy,dbus_interface="org.freedesktop.NetworkManager");
        devices=self.nm.GetDevices()
        self.wireless = None
        self.ap=None
        self.success = True
        for device in devices:
            deviceproxy=self.bus.get_object("org.freedesktop.NetworkManager", device)
            device_iface=dbus.Interface(deviceproxy,dbus_interface=dbus.PROPERTIES_IFACE)
            if device_iface.Get("org.freedesktop.NetworkManager.Device","DeviceType") == 2:
                self.wirelessprop=device_iface
                self.wireless=dbus.Interface(deviceproxy,dbus_interface="org.freedesktop.NetworkManager.Device.Wireless")
                break
        if self.wireless == None:
            print "No Devices Found"
            self.success = False

                    
    def connect(self,ap):
        pass
    
    def findAPbyName(self,ssid):
        '''Finds AP object by name. Returns only AP with most strength
            @return: The DBUS Object representing the IP
        '''
        finap=None
        aps=self.wireless.GetAccessPoints()
        polimis=[]
        for ap in aps:
            aproxy=self.bus.get_object("org.freedesktop.NetworkManager", ap)
            aprop=dbus.Interface(aproxy,dbus.PROPERTIES_IFACE)
            fssid="".join([chr(c) for c in aprop.Get("org.freedesktop.NetworkManager.AccessPoint","Ssid")])
            if fssid==ssid:
                polimis.append(ap)
        pmax=0
        if len(polimis)>0:
            for fap in polimis:
                aproxy=self.bus.get_object("org.freedesktop.NetworkManager", fap)
                aprop=dbus.Interface(aproxy,dbus.PROPERTIES_IFACE)
                powert=aprop.Get("org.freedesktop.NetworkManager.AccessPoint","Strength")
                if powert>pmax:
                    pmax= powert
                    finap=fap
        return finap