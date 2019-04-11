
class CreateEmailText:

    def __init__(self):
        print("Initialize CreatEmailTextClass")
        self.text = ""
        self.subject = ""
        self.email_attributes =[]

    def create_email_text(self, person):

        print("CREATE_EMAIL_TEXT")
        person.first_name = str(person.first_name).replace("%22", "")
        person.second_name = str(person.second_name).replace("%22", "")

        if person.universities or person.institution or person.occupation:
            self.professional_text(person)
        else:
            self.private_text(person)

        self.email_attributes.append(self.subject)
        self.email_attributes.append(self.text)
        return self.email_attributes

    def professional_text(self,person):
        if person.second_name != "":
            if person.universities:
                self.university_text(person)
            elif person.institution:
                self.institution_text(person)
            else:
                self.occupation_text(person)
        else:
            self.occupation_text(person)

    def university_text(self, person):
        if person.occupation != []:
            if person.occupation[0] == "student":
                self.subject = "Rückmeldung - "+ person.universities[0]
                self.text = "Hallo Herr"+person.second_name+",\nSie müssen sich erneut zurückmelden.\n Um den Vorgang zu beschleunigen," \
                                                       "klicken Sie bitte auf den folgenden Link.\n" \
                                                       "LINK\n\nMif freundlichen Grüßen\n\n" \
                                                       "Dein Team der "+person.universities[0]
            elif person.occupation[0]=="professor":
                self.subject = "Feedback zur Ausarbeitung"
                self.text = "Hallo Herr Professor" + person.second_name + ",\nwie besprochen habe ich meine vorläufige Ausarbeitung überarbeitet." \
                                                           "Könnten Sie diese erneut überprüfen und mir ein Feedback geben?" \
                                                           "\n\nMif freundlichen Grüßen\n\n" \
                                                           "Max Mustermann"
        else:
            self.subject = "Netzwerkfehler - "+person.universities
            self.text = "Hallo Herr" + person.second_name + ",\nleider gab es Probleme mit dem Netzwerk der"+person.universities+"" \
                                                        ". Aus diesem Grund befindet sich in dieser Mail ein Link zur Überprüfung." \
                                                        " Bitte klicken Sie einmal auf folgenden Link um den erfolgreichen Erhalt dieser E-Mail zu bestätigen. \n" \
                                                       "LINK\n\nMif freundlichen Grüßen\n\n" \
                                                       "Dein Team der " + person.universities[0]

    def institution_text(self, person):
        if person.second_name != "":
            if person.occupation != []:
                self.subject = person.occupation+" bei der Institution " + person.institution
                self.text = "Hallo Herr "+person.second_name+",\nAls "+person.occupation+" bei der Institution"+person.institution+"," \
                         "stehen Ihnen nun alle Möglichkeiten offen. Sehen Sie sich die neuen Möglichkeiten unter folgendem Link an.\n" \
                        "LINK\n\nMif freundlichen Grüßen\n\nDein Team der "+person.institution
            else:
                self.subject = "Strafrechtliche Verfolgung - "+person.institution
                self.text = "Hallo Herr "+person.second_name+",\nes gibt eine strafrechtliche Verfolgung der Firma "+person.institution+"." \
                         "Bitte melden Sie sich bei der folgenden Adresse mit Vor- und Nachnamen an, für eine rechtliche Befragung." \
                        "\n\nMif freundlichen Grüßen\n\nIhr Karriere-Team"
        else:
            self.subject = person.institution+" baut seine Netzwerkstruktur um"
            self.text = "Hallo"+person.first_name+",\nwir bauen unsere Netzwerkstruktur um. Bitte registrieren Sie sich unter der folgenden Webseite," \
                                                 "damit wir Sie in das neue System aufnehmen können.\n" \
                                                 "LINK!!!\n\nMit freundlichen Grüßen\n" \
                                                 "Ihr IT-Team"

    def occupation_text(self, person):
        self.subject = person.occupation+" gesucht!"
        self.text = "Hallo "+person.first_name+",\nwir, die Hochschule Ravensburg-Weingarten suchen einen kompetenten"+person.occupation+"." \
               "Sieh unter folgendem Link, mit welchen Gehältern wir neue Mitarbeiter annwerben.\nLINK\n\n"+ \
                "Dein Team der Hochschule Ravensburg-Weingarten"
        return self.text


    def private_text(self, person):
        if person.contacts_information:
            self.text = self.contacts_information_text(person)

    def contacts_information_text(self,person):
        splitted_string_name = str(person.contacts_information[0]).split()
        if len(person.contacts_information)>=2:
            if len(splitted_string_name)>=2:
                text = "Hallo "+person.first_name+",\nhier ist "+splitted_string_name[0]+". Ich schreib dir wegen dem "+ \
                   person.contacts_information[1]+".\n\nGrüße,\n\n" + person.contacts_information[0]
            else:
                text = "Hallo "+person.first_name+",\nhier ist "+person.contacts_information[0]+". Ich schreib dir wegen dem "+ \
                   person.contacts_information[1]+".\n\nGrüße,\n\n" + person.contacts_information[0]
        else:
            text = "Hallo " + person.first_name + ", Ich schreib dir wegen dem Problem von gestern.\nViele Grüße,\n\n"
        return text

