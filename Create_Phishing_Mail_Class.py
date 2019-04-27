import Create_Email_Addresses_Class
import Create_Email_Text_Class
import Send_Email_Class


class CreatePhishingMail:

    def __init__(self):
        self.destination_address = []
        self.email_attributes = ""

    def create_phishing_mail(self, person):
        if not person.input_email:
            if not person.mails_found:
                create_email_addresses_class = Create_Email_Addresses_Class.CreateEmailAddresses()
                self.destination_address = create_email_addresses_class.create_email_addresses(person)
            else:
                self.destination_address = person.mails_found
        else:
            self.destination_address.append(person.input_email)
        create_email_text_class = Create_Email_Text_Class.CreateEmailText()
        self.email_attributes = create_email_text_class.create_email_text(person)
        send_email_class = Send_Email_Class.SendEmailClass()
        send_email_class.send_mail(self.email_attributes[0], self.email_attributes[1])

        print("Phishing-Mail:\n\nSUBJECT: ", self.email_attributes[0])
        print(self.email_attributes[1])
