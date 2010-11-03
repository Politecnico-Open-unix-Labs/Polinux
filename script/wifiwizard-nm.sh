#!/bin/bash
# 
# Author: Sante Rotondi <saten.r@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 

if [ -z $(which gksudo) ]
then
	if [ -z $(which zenity) ]
	then
		echo "Impossibile proseguire. Questo script richiede che zenity, gksu, openssl e nm-applet siano installati."
		exit 1
	else
	zenity --error --text="Impossibile proseguire. Questo script richiede che zenity, gksu, openssl e nm-applet siano installati."
	exit 1
	fi
	exit
fi

gksudo bash `dirname $0`/wifiwizard-nm-sudo.sh

if [ $? -eq 0 ]
then
	if [ `grep -c BEGIN /etc/asi.cer` -lt 2 ]
	then
		exit
	fi
	if [ ! -e /tmp/template.xml ]
	then
		exit
	fi
	gconftool-2 --load /tmp/template.xml
	zenity --warning --text="Configurazione completata.
	
<b>Importante:</b>
Se si è connessi alla rete <b>\"polimi\"</b>, prima di collegarsi alla rete <b>\"internet\"</b> è necessario disconnettersi.
	
Cliccare con il tasto destro sull'icona di network manager (accanto all'orologio) e selezionare \"Modifica connessioni\".
	
Cliccare su \"wireless\" e rimuovere la connessione a \"polimi\"."
elif [ $? -eq 1 ]
then
	zenity --error --text="Errore. Non è stato possibile concludere la configurazione."
fi

exit
