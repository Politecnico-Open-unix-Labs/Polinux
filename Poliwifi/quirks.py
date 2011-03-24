'''
Created on 21/mar/2011
GPLv3
@author: admiral0
'''
import  ConfigParser,sys
INTERNET_PATH="/etc/NetworkManager/system-connections/internet"

brick=open(INTERNET_PATH,'r+')
config=ConfigParser.ConfigParser()
config.readfp(brick)
try:
    config.get("802-1x","private-key")
except ConfigParser.NoOptionError,ConfigParser.NoSectionError:
    config.set("802-1x", "private-key", sys.argv[1])
    
try:
    config.get("802-1x","private-key-password")
except ConfigParser.NoOptionError,ConfigParser.NoSectionError:
    config.set("802-1x", "private-key-password", sys.argv[2])

if sys.argv[3]=="0":
    try:
        config.get("connection","autoconnect")
    except ConfigParser.NoOptionError,ConfigParser.NoSectionError:
        config.set("connection", "autoconnect", "FALSE")
        
brick.close()