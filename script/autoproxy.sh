#!/bin/bash
# 
# Author: Sante Rotondi <saten.r@gmail.com>
# Contributor: Radu Andries <admiral0@tuxfamily.org>
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

# un po' di pulizia
unset http_proxy
unset ftp_proxy
#unset auto_proxy
unset HTTP_PROXY
unset FTP_PROXY
#unset AUTO_PROXY
unset POLIHOST
OFFLINE=0
TIMEOUT=600
#debug
#TIMEOUT=1
FILEWPAD=$(mktemp)
unlink $FILEWPAD
FILESVN=$(mktemp)
unlink $FILESVN
function getit {
		# uso route -n per determinare se sono connesso a qualcosa
		# greppare su UG conta solo i gateway
		# route -n non fa perdere tempo nel risolvere
		if [ $(route -n | grep UG | wc -l) -gt 0 ]
			then
			#echo abbiamo almeno un gateway impostato
			# qui potremmo fare un check di raggiungibilità di wpad.polimi.it
			# il ping no.. pianta tutto
			host wpad.polimi.it 1>/dev/null
			POLIHOST=$_	
			#echo $POLIHOST
			if [ $POLIHOST == "wpad.polimi.it" ]
				then
				#echo "ho risolto il proxy address"
				#cd /tmp
				wget http://wpad.polimi.it/wpad.dat -O $FILEWPAD 2>/dev/null
				#cat $FILEWPAD
				#cd - >/dev/null
				OFFLINE=1
			fi
		else
			OFFLINE=0
		fi		
}

# some caching here
# se il file esiste ed ha più di dieci minuti, controllo
# altrimenti immagino di essere ancora a casa/poli ed evito di perdere tempo
if [ -f $FILEWPAD ]
	then
	#echo "il file esiste"
	FILEDATE=$(date --utc --reference=$FILEWPAD +%s )
	DATE=$(date --utc +%s)
	DIFFDATE=$(($DATE-$FILEDATE))
	#echo "file scaricato " $DIFFDATE " secondi fa"
	if [ $DIFFDATE -gt $TIMEOUT ]
		then
		rm $FILEWPAD
		getit
	fi
else
	getit
fi
if [ -f $FILEWPAD ]
	then
	LINES=$(wc -l $FILEWPAD | sed "s#$FILEWPAD##g")
	#echo "wpad lines: "$FILEWPAD $LINES
	if [ $LINES -lt 50 ]
		then
		#echo "sono nella rete del poli, wpad.dat ha poche linee"
		# esportiamo tutte le variabili d'ambiente del caso
		export http_proxy="http://proxy.polimi.it:8080"
                export https_proxy="http://proxy.polimi.it:8080"
		export ftp_proxy="http://proxy.polimi.it:8080"
		export auto_proxy="http://wpad.polimi.it/wpad.dat"
		export HTTP_PROXY="http://proxy.polimi.it:8080"
		export HTTPS_PROXY="http://proxy.polimi.it:8080"
		export FTP_PROXY="http://proxy.polimi.it:8080"
		export AUTO_PROXY="http://wpad.polimi.it/wpad.dat"
		#echo settiamo il proxy per subversion
		#cp /home/$USER/.subversion/servers /tmp/servers.$USER
		if [ -f /home/$USER/.subversion/servers ] && [ $(fgrep -c polimi /home/$USER/.subversion/servers ) -eq 0 ]
			then
			cat /etc/polinux/svn.proxy /home/$USER/.subversion/servers > $FILESVN
			cp $FILESVN /home/$USER/.subversion/servers
		fi
	else
		#echo "non siamo nella rete del poli, liberi tutti :D"
		unset http_proxy
		unset ftp_proxy
		#unset auto_proxy
		unset HTTP_PROXY
		unset FTP_PROXY
		#unset AUTO_PROXY
		#echo ripristiniamo il file di configurazione di subversion
		if [ -f /home/$USER/.subversion/servers ] && [ $( fgrep -c polimi /home/$USER/.subversion/servers ) -eq 1 ]
			then
			# questa fraccata di sed funziona ma fa un po' schifo, si accettano proposte più eleganti ;)
			# secondo me, ma ora sono offline, si può fare il tutto con patch ;D
			sed -i '1{s/\[global\]//}' /home/$USER/.subversion/servers
			sed -i '2{s/http-proxy-host\ =\ proxy.polimi.it//1}' /home/$USER/.subversion/servers			 
			sed -i '3{s/http-proxy-port\ =\ 8080//1}' /home/$USER/.subversion/servers
			sed -i '1,/^./{/./!d}' /home/$USER/.subversion/servers
		fi
	fi
	cd >/dev/null
#elif [ $OFFLINE -eq 0 ]
#	then
#	echo "non è stato possibile configurare il proxy, controllare la rete"
fi
