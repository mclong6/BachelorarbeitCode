import re
class CreateEmailText:

    def __init__(self):
        self.text = ""
        self.subject = ""
        self.email_attributes =[]
        self.salutation = ""

    def create_email_text(self, person):
        if person.first_name != "" and person.second_name != "" and person.sex:
            person.first_name = str(person.first_name).replace("%22", "").capitalize()
            person.second_name = str(person.second_name).replace("%22", "").capitalize()
            if person.sex == "w":
                self.salutation = "Frau"
            else:
                self.salutation = "Herr"
            if person.contacts_information:
                if person.contacts_information:
                    self.contacts_information_text(person)
            elif person.institutions_found or person.institution or person.occupation:
                self.professional_text(person)
            else:
                self.private_text(person)
        else:
            self.subject = "Random Subject"
            self.text = "Random Text - No information"

        self.email_attributes.append(self.subject)
        self.email_attributes.append(self.text)
        return self.email_attributes

    def professional_text(self,person):
        if person.second_name != "":
            if person.institutions_found:
                self.institution_text(person, True)
            elif person.institution:
                self.institution_text(person, False)

            else:
                self.occupation_text(person)
        else:
            self.occupation_text(person)

    def institution_text(self, person, key):
        if key:
            institution = person.institutions_found
        else:
            institution = person.institution
        institution = re.sub(r'\b[a-z]', lambda m: m.group().upper(), str(institution))

        person.second_name = str(person.second_name).capitalize()
        person.first_name = str (person.second_name).capitalize()
        if person.second_name != "":
                if person.occupation != "":
                    person.occupation = str(person.occupation).capitalize()
                    if person.occupation == "Student":
                        self.subject = "Rückmeldung - " + institution
                        self.text = "Hallo "+self.salutation+" " + person.second_name + ",\nleider ist und ein Fehler unterlaufen. Aus diesem Grund müssen sie sich erneut" \
                                                                                        "zurückmelden.\n Um den Vorgang zu beschleunigen," \
                                                                        " klicken Sie bitte auf den folgenden Link.\n" \
                                                                        "https://badlink.com\n\nMit freundlichen Grüßen\n\n" \
                                                                        "Ihr Studentenservice der " + institution
                    elif person.occupation == "Professor":
                        self.subject = "Feedback zur Ausarbeitung"
                        self.text = "Hallo "+self.salutation+" Professor " + person.second_name + ",\nwie besprochen befindet sich im Anhang meine vorläufige Ausarbeitung.\n" \
                                                                                  "Könnten Sie diese erneut überprüfen und mir ein Feedback geben?" \
                                                                                  "\n\nMif freundlichen Grüßen\n\n" \
                                                                                  "Max Mustermann"
                    else:
                        self.subject = person.occupation+" bei der " + institution
                        self.text = "Hallo "+self.salutation+" "+person.second_name+",\nals "+ person.occupation+" bei der "+institution+"," \
                                 " stehen Ihnen nun alle Möglichkeiten offen. Sehen Sie sich die neuen Möglichkeiten unter folgendem Link an.\n" \
                                "https://badlink.com\n\nMit freundlichen Grüßen\n\nIhr Karriere-Team der "+institution
                else:
                    self.subject = institution + " - Netzwerkänderungen"
                    self.text = "Hallo "+self.salutation+" " + person.second_name + ",\nwir bauen unsere Netzwerkstruktur um. Bitte registrieren Sie sich unter der folgenden Webseite," \
                                                                "damit wir Sie in das neue System aufnehmen können.\n" \
                                                                "https://badlink.com\n\nMit freundlichen Grüßen\n\n" \
                                                                "Ihr IT-Team der " + institution


    def occupation_text(self, person):
        person.occupation = str(person.occupation).capitalize()
        person.second_name = str (person.second_name).capitalize()
        self.subject = person.occupation+" gesucht - Im Auftrage der BRD"
        self.text = "Hallo "+self.salutation+" "+person.second_name+",\ndie Bundesrepublik Deutschland sucht einen kompetenten "+person.occupation+"." \
               "Haben Sie Interesse an einer neuen Herausforderung unter optimalen Arbeitsbedingungen?\n" \
                "Im Anhang finden Sie die offizielle Stellenausschreibung mit den dazugehörigen Voraussetzungen und Gehaltsstufen.\n\n" \
                "Ihr Karriere-Team der Bundesrepublik Deutschland"

    def private_text(self, person):
        if person.year_of_birth!= "":
            self.year_of_birth_text(person)
        elif person.hobbies != "":
            self.hobby_text(person)
        elif person.locations != "":
            self.locations_text(person)

    def contacts_information_text(self,person):
        splitted_string_name = str(person.contacts_information[0]).split()
        if len(person.contacts_information)>=2:
            self.subject = "Fragen bzgl. "+ person.contacts_information[1]
            if len(splitted_string_name)>=2:
                self.text = "Hi "+person.first_name+",\nhier ist "+splitted_string_name[0]+". Bezüglich  "+ \
                   person.contacts_information[1]+" hätte ich noch ein paar fragen an dich...\n" \
                                                  "Könntest du zufällig in den Anhang schauen und bewerten was ich da so rausgesucht habe?" \
                                                  ".\n\nGrüße,\n\n" + person.contacts_information[0]
            else:
                self.text = "Hi " + person.first_name + ",\nhier ist " + splitted_string_name[0] + ". Bezüglich " + \
                       person.contacts_information[1] + " hätte ich noch ein paar fragen an dich...\n" \
                                                        "Könntest du zufällig in den Anhang schauen und bewerten was ich da so rausgesucht habe?" \
                                                        "\n\nGrüße,\n\n" + person.contacts_information[0]
    def hobby_text(self,person):
        self.subject = "Verbessere deine Technik im "+person.hobbies
        self.text = "Hi "+person.first_name+",\n damit du deine Leistung im"+person.hobbies+" verbessern kannst, musst du unbedingt" \
                                                                                            "die Techniken deiner Vorbilder anschauen!\n" \
                                                                                            "Im Anhang befindet sich eine kleine Übersicht.\n\n" \
                                                                                            "Dein Team der deutschen Förderung"
    def year_of_birth_text(self,person):
        if person.locations != "":
            self.subject = "Jahrgang "+person.year_of_birth+" - "+person.locations
            self.text = "Hi"+ person.first_name+",\n dieses Jahr findet in "+person.locations+" ein Treffen für alle Personen, die "+person.year_of_birth+"" \
                        " geboren sind, statt. Im Anhang befindet sich eine Liste mit den Leuten die bereits zugesagt haben.\n\n" \
                        "Dein Orga-Team "+person.locations
        else:
            self.subject = "Jahrgang " + person.year_of_birth
            self.text = "Hi" + person.first_name + ",\n dieses Jahr findet ein Treffen für alle Personen, die " + person.year_of_birth + "" \
                        " geboren sind, statt. Im Anhang befindet sich eine Liste mit den Leuten die bereits zugesagt haben.\n\n" \
                        "Dein Orga-Team"
    def locations_text(self,person):
        self.subject = "Streetfood-Festival in "+person.locations
        self.text = "Hi "+ person.first_name+"dieses Jahr findet das erste STREETFOOD-FESTIVAL in "+person.locations+ "" \
                    " statt. Im Anhang befindet sich der Plan, auf dem alles weitere erklärt wird.\n" \
                    "Wir freuen uns auf dich!\n\nDein Streefood-Team aus "+person.locations
