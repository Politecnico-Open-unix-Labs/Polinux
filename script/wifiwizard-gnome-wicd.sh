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
	echo "Zenity non è installato. Impossibile proseguire. Questo script richiede che zenity, openssl e wicd siano installati."
	exit
fi

if [ `whoami` != "root" ] 
then
	zenity --error --text="Questo programma deve essere eseguito come amministratore."
	exit
fi

if [ -z $(which wicd) ]
then
	zenity --error --text="wicd non è installato. Impossibile proseguire. Questo script richiede che zenity, openssl e wicd siano installati."
	exit
fi


if [ -z $(which openssl) ]
then
	zenity --error --text="openssl non è installato. Impossibile proseguire. Questo script richiede che zenity, openssl e wicd siano installati."
	exit
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
exit
fi
ifconfig $WIFI_INTERFACE up

zenity --question --title "Configurazione guidata rete" --text "<b>Benvenuto nello script di configurazione per la rete senza fili \"internet\".</b>

Se non disponi del file CertificatoASI.p12 ti consiglio di premere il tasto annulla, connetterti alla rete "polimi" ed aprire firefox. Si aprirà automaticamente la pagina con le istruzioni.

<b>Per utilizzare questo programma è sufficiente avere a disposizione il certificato.</b>

Non è necessario seguire la guida per Linux presente sul sito dell'ASI. La guida per utilizzare questo script si trova nella cartella /usr/share/doc/polinux-desktop.

Ti sarà ora richiesto di selezionare il file CertificatoASI.p12, inserire il tuo numero di matricola e la password che hai scelto per il Certificato."
if [ $? -eq 1 ]
then
	exit
fi
zenity --question --title="Domanda" --text="Hai già creato e scaricato il certificato (o disponi del tuo certificato su una chiavetta/cartella) su questo pc?

Premendo Annulla si verrà connessi alla rete \"polimi\" e si aprirà la pagina per la creazione del certificato."
if [ $? -eq 1 ]
then
        if [ ! -z "$WIFI_INTERFACE" ]
        then
                ifconfig $WIFI_INTERFACE down
                ifconfig $WIFI_INTERFACE up
                iwconfig $WIFI_INTERFACE essid polimi
                dhclient $WIFI_INTERFACE
        else
                zenity --error --title="Errore" --text="<b>Non sono in grado di trovare la tua scheda senza fili.</b>

Per favore controlla che questa sia accesa o collegata."
		exit
		fi

	exec firefox https://www.asi.polimi.it/rete/wifi/richiesta_certificato.html &
	exit
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

cp $CERTP12 /etc/CertificatoASI.p12

if [ ! -e /etc/CertificatoASI.p12 ]
then
	zenity --error --text "Si è verificato un errore nella gestione del certificato. Controllare lo spazio libero ed i permessi dell'utente."
       	exit
fi

openssl pkcs12 -cacerts -in /etc/CertificatoASI.p12 -out /etc/asi.cer -passin pass:$PWD -passout pass:$PWD

if [ `grep -c BEGIN /etc/asi.cer` -lt 2 ]
then
	zenity --error --text "I dati inseriti per il certificato non sono corretti, riprovare."
	exit
else

echo "name = POLIMI
author = Sante Gennaro Rotondi
version = 1
require password *Password_del_certificato
----
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
network={
ssid=\"internet\"
proto=WPA
key_mgmt=WPA-EAP
auth_alg=OPEN
pairwise=TKIP
eap=TLS
anonymous_identity=\"$MATRICOLA\"
ca_cert=\"/etc/asi.cer\"
private_key=\"/etc/CertificatoASI.p12\"
private_key_passwd=\"\$_PASSWORD\"
phase2=\"auth=MSCHAPV2\"
}

" > POLIMI
mv POLIMI /etc/wicd/encryption/templates/POLIMI
cat /etc/wicd/encryption/templates/active | grep -v POLIMI > foo
echo "POLIMI" >> foo
mv foo /etc/wicd/encryption/templates/active 
chmod +r /etc/CertificatoASI.p12
chmod +r /etc/asi.cer
zenity --info --text "<b>Configurazione completata. Adesso verrà eseguito wicd-client per effettuare la configurazione.</b>

Clicca la freccia verso il basso situata in alto a sinistra e seleziona Hidden Network.

Inserisci il testo \"internet\" senza apici nella finestra di richiesta.
Clicca il triangolo bianco a sinistra della rete internet, poi \"Impostazioni avanzate\".

Seleziona la casella di \"Utilizza cifratura\" e nel menu sotto di essa seleziona \"<b>POLIMI</b>\".

Nel campo \"Password del certificato\" reimmettere la password.

E' possibile tenere aperta questa finestra per leggere queste istruzioni durante la configurazione di wicd.

<b>In caso di mancata connessione, controllare che la rete internet sia tra quelle disponibili e che la scheda wireless impostata nelle preferenze di wicd sia $WIFI_INTERFACE.</b>
" --title "Configurazione certificato completata"&
sleep 7
wicd-client -n
fi

