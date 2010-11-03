#!/usr/bin/python

from mechanize import Browser
import io

bro = Browser()
bro.set_handle_robots(0)     
response=bro.open('https://www.asi.polimi.it/rete/wifi/richiesta_certificato.html')
response=bro.follow_link(text='logon')
bro.select_form('')
bro.form['login']='matricola'
bro.form['password']='password'
bro.submit()
response=bro.open('https://www.asi.polimi.it/rete/wifi/richiesta_certificato.html')
response=bro.follow_link(text='nuovo certificato')
bro.select_form(name='exists')
bro.submit()
bro.select_form(name='passphrase')
bro.form['passphrase']='thepassphrase'
bro.form['passphraseCheck']='thepassphrase'
tempfile=bro.retrieve(bro.form.click('_qf_passphrase_next'))
response=bro.open('http://www.asi.polimi.it/util/download.html?type=certificato')
io.os.unlink(tempfile[0])
f= file('/tmp/CertificatoASI.p12','wb')
while 1:
  data=response.read(1024)
  if not data:
    break
  f.write(data)
f.close()

