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

if [ -z $(which zenity) ]
then
	echo "Zenity non è installato. Impossibile proseguire. Questo script richiede che zenity, gksu, openssl e nm-applet siano installati."
	exit 1
fi

if [ `whoami` != "root" ] 
then
	zenity --error --text="Questo programma deve essere eseguito come amministratore."
	exit 1
fi
if [ -z $(which nm-applet) ]
then
	zenity --error --text="nm-applet (networkmanager-gnome) non è installato. Impossibile proseguire. Questo script richiede che zenity, gksu, openssl e nm-applet siano installati."
	exit 1
fi


if [ -z $(which openssl) ]
then
	zenity --error --text="openssl non è installato. Impossibile proseguire. Questo script richiede che zenity, gksu, openssl e nm-applet siano installati."
	exit 1
fi

CERTP12="null"
MATRICOLA=''
TIPOLOGIA=''
PWD=''

WIFI_INTERFACE=$(iwlist scan 2>/dev/null  | grep "completed" | sed s/"     Scan completed :"/""/)

if [ -z "$WIFI_INTERFACE" ]
	then
    WIFI_INTERFACE=$(iwlist scan 2>/dev/null | grep "results" | sed s/"     No scan results"/""/)
fi
if [ -z "$WIFI_INTERFACE" ]
	then
    zenity --error --title="Errore" --text="<b>Non sono in grado di trovare la tua scheda senza fili.</b>

Per favore controlla che questa sia accesa o collegata."
exit 1
fi
ifconfig $WIFI_INTERFACE up

zenity --question --title "Configurazione guidata rete" --text "<b>Benvenuto nello script di configurazione per la rete senza fili \"internet\".</b>

Se non disponi del file CertificatoASI.p12 ti consiglio di premere il tasto annulla, connetterti alla rete "polimi" ed aprire firefox. Si aprirà automaticamente la pagina con le istruzioni.

<b>Per utilizzare questo programma è sufficiente avere a disposizione il certificato.</b>

Non è necessario seguire la guida per Linux presente sul sito dell'ASI.

Ti sarà ora richiesto di selezionare il file CertificatoASI.p12, inserire il tuo numero di matricola e la password che hai scelto per il Certificato."
if [ $? -eq 1 ]
then
	exit 1
fi

if [ -e /tmp/template.xml ]
then
	rm /tmp/template.xml
fi
while  [ ! -e $CERTP12 ]
do
	CERTP12=$(zenity --title="Seleziona il file Certificato.p12" --filename="CertificatoASI.p12" --file-selection)
	if [ $? -eq 1  ]
	then
		 exit
	fi
	if [ ! -e $CERTP12 ]
	then
	 	zenity --error --title "Errore" --text "Selezionare il certificato corretto"
	fi
done
while [ -z $TIPOLOGIA ]
do
	TIPOLOGIA=$(zenity  --list --title "Selezionare tipologia utente"  --radiolist  --column "" --column "Tipo di utente" TRUE Studente FALSE Visitatore FALSE "Utente Tecnico - Amministrativo" FALSE Docente)
        if [ $? -eq 1  ]
        then
		 exit
	fi
		 TIPOLOGIA=${TIPOLOGIA:0:1}
done
while [ -z $MATRICOLA ]
do
	MATRICOLA=$(zenity --title="Matricola" --text="Inserisci il tuo numero di Matricola" --entry);
        if [ $? -eq 1  ]
        then exit
	fi
	if [ -z $MATRICOLA ]
		then
	        zenity --error --text "La matricola non può essere vuota."
	fi
done
MATRICOLA=$TIPOLOGIA$MATRICOLA
while [ -z $PWD ]
do
	PWD=$(zenity --entry --hide-text --title="Password" --text="Inserisci la password del certificato")
    if [ $? -eq 1  ]
        then exit
    fi
	if [ -z $PWD ]
		then
	        zenity --error --text "La password non può essere vuota."
	fi
done
if [ ! $CERTP12 = "/etc/CertificatoASI.p12" ]
    then
    if [ -e /etc/CertificatoASI.p12 ]
        then
        rm -f /etc/CertificatoASI.p12    
    fi
fi

cp $CERTP12 /etc/CertificatoASI.p12

if [ -e /etc/asi.cer ]
then
        rm -f /etc/asi.cer
fi

if [ ! -e /etc/CertificatoASI.p12 ]
then
	zenity --error --text "Si è verificato un errore nella gestione del certificato. Controllare lo spazio libero ed i permessi dell'utente."
    exit 2
fi

openssl pkcs12 -cacerts -in /etc/CertificatoASI.p12 -out /etc/asi.cer -passin pass:$PWD -passout pass:$PWD

if [ `grep -c BEGIN /etc/asi.cer` -lt 2 ]
then
	zenity --error --text "I dati inseriti per il certificato non sono corretti, riprovare."
	exit
fi
chmod +r /etc/CertificatoASI.p12
chmod +r /etc/asi.cer
if [ -d /home/$SUDO_USER/.gconf/system/networking/connections ]
then 
	cd /home/$SUDO_USER/.gconf/system/networking/connections
	for FOLDER in $(ls | grep -v %gconf.xml)
	do
	    echo "NetworkManager already configured connection:" $FOLDER
	done
	let "NUMBER= $FOLDER +1"
else 
	let "NUMBER = 1"
fi
#else 
#	mkdir -p /home/$SUDO_USER/.gconf/system/networking/connections
#	cd /home/$SUDO_USER/.gconf/system/networking/connections


echo "
<gconfentryfile>
  <entrylist base=\"/system/networking/connections\">
    <entry>
      <key>$NUMBER/802-11-wireless/name</key>
      <value>
        <string>802-11-wireless</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-11-wireless/security</key>
      <value>
        <string>802-11-wireless-security</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-11-wireless/ssid</key>
      <value>
        <list type=\"int\">
            <value>
              <int>105</int>
            </value>
            <value>
              <int>110</int>
            </value>
            <value>
              <int>116</int>
            </value>
            <value>
              <int>101</int>
            </value>
            <value>
              <int>114</int>
            </value>
            <value>
              <int>110</int>
            </value>
            <value>
              <int>101</int>
            </value>
            <value>
              <int>116</int>
            </value>
        </list>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-11-wireless-security/key-mgmt</key>
      <value>
        <string>wpa-eap</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-11-wireless-security/name</key>
      <value>
        <string>802-11-wireless-security</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/eap</key>
      <value>
        <list type=\"string\">
            <value>
              <string>tls</string>
            </value>
        </list>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/identity</key>
      <value>
        <string>$MATRICOLA</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/name</key>
      <value>
        <string>802-1x</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/nma-path-ca-cert</key>
      <value>
        <string>/etc/asi.cer</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/nma-path-client-cert</key>
      <value>
        <string>/etc/CertificatoASI.p12</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/802-1x/nma-path-private-key</key>
      <value>
        <string>/etc/CertificatoASI.p12</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/connection/autoconnect</key>
      <value>
        <bool>true</bool>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/connection/id</key>
      <value>
        <string>internet</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/connection/name</key>
      <value>
        <string>connection</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/connection/type</key>
      <value>
        <string>802-11-wireless</string>
      </value>
    </entry>
    <entry>
      <key>$NUMBER/connection/uuid</key>
      <value>
        <string>444d984f-672a-46f7-8085-c9c9259be40f</string>
      </value>
    </entry>
  </entrylist>
</gconfentryfile>
" > /tmp/template.xml
#sudo -E -u $SUDO_USER gconftool-2 --load ./template.xml
exit
