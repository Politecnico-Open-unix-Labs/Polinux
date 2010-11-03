name = POLIMI
author = Sante Gennaro Rotondi
version = 1
require password *Password_del_certificato
----
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
network={
ssid="internet"
proto=WPA
key_mgmt=WPA-EAP
auth_alg=OPEN
pairwise=TKIP
eap=TLS
anonymous_identity="%MATRICOLA%"
ca_cert="/etc/asi.cer"
private_key="/etc/CertificatoASI.p12"
private_key_passwd="$_PASSWORD"
phase2="auth=MSCHAPV2"
}
