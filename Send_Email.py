

import smtplib
from email.mime import multipart
from email.mime import text

senderEmail = 'bachelorarbeit2@gmx.de'
empfangsEmail = 'marcolang95@web.de'
password = 'bachelorarbeit2'

msg = multipart.MIMEMultipart()
msg['From'] = senderEmail
msg['To'] = empfangsEmail
msg['Subject'] = 'Deine Pflanze verdurstet'

emailText = 'Diese Email kommt von PYTHON'
msg.attach(text.MIMEText(emailText, 'html'))

server = smtplib.SMTP('mail.gmx.net', 587) # Die Server Daten
server.ehlo()
server.starttls()
server.login(senderEmail, password) # Das Passwort
text = msg.as_string()
server.sendmail(senderEmail, empfangsEmail, text)
server.quit()
