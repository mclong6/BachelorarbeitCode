import Create_Email_Addresses_Class
import Create_Email_Text_Class


class CreatePhishingMail:

    def __init__(self):
        print("Initialize CreatePhishingMail")
        self.destination_adress = []
        self.email_text = ""

    def create_phishing_mail(self, person):
        if not person.input_email:
            if not person.founded_mails:
                create_email_adresses_class = Create_Email_Addresses_Class.CreateEmailAddresses()
                self.destination_adress = create_email_adresses_class.create_email_addresses(person)
            else:
                self.destination_adress = person.founded_mails
        else:
            self.destination_adress.append(person.input_email)
        create_email_text_class = Create_Email_Text_Class.CreateEmailText()
        self.email_text = create_email_text_class.create_email_text(person)

        print(self.destination_adress)
        print(self.email_text)


'''
class Person(object):
    def __init__(self):
        self.first_name = input("Vorname: ").replace(" ", "%22").lower()
        self.second_name = input("Nachname: ").replace(" ", "%22").lower()
        self.place_of_residence = input("Wohnort: ").replace(" ", "%22").lower()
        self.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ", "%22")
        self.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ", "%22")
        self.institution = input("Institution: ").replace(" ", "%22")
        self.instagram_name = input("Instagram Benutzername: ")
        self.facebook_name = input("Facebook Benutzername: ")
        self.twitter_name = input("Twitter Benutzername: ")
        self.input_email = input("E-Mail-Adresse: ")
        self.occupation = []
        self.hobbies = []
        self.universities = ["FH-Weingarten"]
        self.founded_mails = []
        self.locations = []
        self.contacts_information = ["Lorenz Büffel", "singen"]

person = Person()
createPhishingMail = CreatePhishingMail()
createPhishingMail.create_phishing_mail(person)
'''