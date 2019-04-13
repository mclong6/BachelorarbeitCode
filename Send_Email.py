

import smtplib
from email.mime import multipart
from email.mime import text

source_email = 'bachelorarbeit2@gmx.de'
destination_email = 'marcolang95@web.de'
password = 'bachelorarbeit2'
subject = 'Deine Pflanze verdurstet'
email_text = 'Diese Email kommt von PYTHON'

msg = multipart.MIMEMultipart()
msg['From'] = source_email
msg['To'] = destination_email
msg['Subject'] = subject

emailText = email_text
msg.attach(text.MIMEText(emailText, 'html'))

server = smtplib.SMTP('mail.gmx.net', 587)
server.ehlo()
server.starttls()
server.login(source_email, password)
text = msg.as_string()
server.sendmail(source_email, destination_email, text)
server.quit()
