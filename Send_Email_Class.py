import smtplib
from email.mime import multipart
from email.mime import text

class SendEmailClass():
    def __init__(self):
        self.source_email = 'bachelorarbeit2@gmx.de'
        self.destination_email = 'bachelorarbeit2@gmx.de'
        self.password = 'bachelorarbeit2'
        self.subject = ''
        self.email_text = ''
        self.msg = multipart.MIMEMultipart()
        self.msg['From'] = self.source_email
        self.msg['To'] = self.destination_email

    def send_mail(self, subject, email_text):
        self.msg['Subject'] = subject
        self.emailText = email_text

        self.msg.attach(text.MIMEText(self.emailText, 'plain'))

        server = smtplib.SMTP('mail.gmx.net', 587)
        server.ehlo()
        server.starttls()
        server.login(self.source_email,self. password)
        text_msg = self.msg.as_string()
        server.sendmail(self.source_email, self.destination_email, text_msg)
        server.quit()
