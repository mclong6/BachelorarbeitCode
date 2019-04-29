import re


# This class creates all email texts and subjects for the phishing mail
class CreateEmailText:

    def __init__(self):
        self.text = ""
        self.subject = ""
        self.email_attributes =[]
        self.salutation = ""

    # check what information is known, if to less information is known, a random text and
    # random subject will be selected
    def create_email_text(self, person):

        if person.sex != "":
            if person.sex == "w":
                self.salutation = "Frau"
            else:
                self.salutation = "Herr"
            if person.first_name != "" and person.second_name != "":
                person.first_name = str(person.first_name).replace("%22", "").capitalize()
                person.second_name = str(person.second_name).replace("%22", "").capitalize()
                if person.contacts_information:
                    if person.contacts_information:
                        self.contacts_information_text(person)
                elif person.institutions_found or person.institution or person.occupation:
                    self.professional_text(person)
                else:
                    self.private_text(person)
            elif person.first_name != "":
                if person.sex == "w":
                    self.salutation = "Frau"
                else:
                    self.salutation = "Herr"
                self.private_text(person)
            else:
                self.subject = "Random Subject"
                self.text = "Random Text - No information"
        else:
            self.subject = "Random Subject"
            self.text = "Random Text - No information"

        self.email_attributes.append(self.subject)
        self.email_attributes.append(self.text)
        return self.email_attributes

    # this method generates texts for a professional phishing mail
    def professional_text(self,person):
        if person.second_name != "":
            if person.institutions_found:
                self.institution_text(person, True)
            elif person.institution:
                self.institution_text(person, False)

            elif person.occupation:
                self.occupation_text(person)

    # Texts, if the victim's institution is known.
    def institution_text(self, person, key):
        if key:
            institution = person.institutions_found
        else:
            institution = person.institution
        institution = re.sub(r'\b[a-z]', lambda m: m.group().upper(), str(institution))

        person.second_name = str(person.second_name).capitalize()
        person.first_name = str (person.second_name).capitalize()
        if person.second_name != "":
                if person.occupation is not None:
                    person.occupation = str(person.occupation).capitalize()
                    if person.occupation == "Student":
                        self.subject = "Rückmeldung - " + institution
                        self.text = "Hallo "+self.salutation+" " + person.second_name + ",\nleider ist und ein Fehler " \
                                    "unterlaufen. Aus diesem Grund müssen sie sich erneut zurückmelden.\n Um den " \
                                    "Vorgang zu beschleunigen, klicken Sie bitte auf den folgenden Link.\n" \
                                    "https://badlink.com\n\nMit freundlichen Grüßen\n\n" \
                                    "Ihr Studentenservice der " + institution

                    elif person.occupation == "Professor":
                        self.subject = "Feedback zur Ausarbeitung"
                        self.text = "Hallo "+self.salutation+" Professor " + person.second_name + ",\nwie besprochen " \
                        "befindet sich im Anhang meine vorläufige Ausarbeitung.\nKönnten Sie diese bitte erneut " \
                        "überprüfen und mir ein Feedback geben?\n\nMif freundlichen Grüßen\n\nMax Mustermann"

                    else:
                        self.subject = person.occupation+" bei der Institution " + institution
                        self.text = "Hallo "+self.salutation+" "+person.second_name+",\nals "+ person.occupation+\
                                    " bei der Institution "+institution+", stehen Ihnen nun alle Möglichkeiten offen. " \
                                    "Sehen Sie sich die neuen Möglichkeiten unter folgendem Link an.\n" \
                                    "https://badlink.com\n\nMit freundlichen Grüßen\n\nIhr Karriere-Team der " \
                                    "Institution "+institution
                else:
                    self.subject = institution + " - Netzwerkänderungen"
                    self.text = "Hallo "+self.salutation+" " + person.second_name + ",\nwir bauen unsere " \
                                "Netzwerkstruktur um. Bitte registrieren Sie sich unter der folgenden Webseite," \
                                "damit wir Sie in das neue System aufnehmen können.\n" \
                                "https://badlink.com\n\nMit freundlichen Grüßen\n\n" \
                                "Ihr IT-Team der Institution" + institution

    # Texts, if the victim's occupation is known.
    def occupation_text(self, person):
        person.occupation = str(person.occupation).capitalize()
        person.second_name = str (person.second_name).capitalize()
        self.subject = person.occupation+" gesucht - Im Auftrage der BRD"
        self.text = "Hallo "+self.salutation+" "+person.second_name+",\ndie Bundesrepublik Deutschland sucht einen " \
                    "kompetenten "+person.occupation+". Haben Sie Interesse an einer neuen Herausforderung unter " \
                    "optimalen Arbeitsbedingungen?\nIm Anhang finden Sie die offizielle Stellenausschreibung mit den " \
                    "dazugehörigen Voraussetzungen und Gehaltsstufen.\n\n" \
                    "Ihr Karriere-Team der Bundesrepublik Deutschland"

    # this method generates texts for a private phishing mail
    def private_text(self, person):
        if person.year_of_birth != "":
            self.year_of_birth_text(person)
        elif person.hobbies != None:
            self.hobby_text(person)
        elif person.locations != None or person.place_of_residence != "":
            self.locations_text(person)

    # Texts, if the victim's contacts information is known.
    def contacts_information_text(self,person):
        splitted_string_name = str(person.contacts_information[0]).split()
        person.contacts_information[1] = str(person.contacts_information[1]).capitalize()
        if len(person.contacts_information)>=2:
            self.subject = "Fragen bzgl. "+ person.contacts_information[1]
            if len(splitted_string_name)>=2:
                self.text = "Hi "+person.first_name+",\nhier ist "+splitted_string_name[0]+". Bezüglich  "+ \
                   person.contacts_information[1]+" hätte ich noch ein paar Fragen an dich...\n" \
                                                  "Könntest du vielleicht in den Anhang schauen und bewerten, was ich " \
                                                  "da so rausgesucht habe?" \
                                                  ".\n\nGrüße,\n\n" + person.contacts_information[0]
            else:
                self.text = "Hi " + person.first_name + ",\nhier ist " + splitted_string_name[0] + ". Bezüglich " + \
                       person.contacts_information[1] + " hätte ich noch ein paar Fragen an dich...\n" \
                                                        "Könntest du vielleicht in den Anhang schauen und bewerten, was " \
                                                        "ich da so rausgesucht habe?" \
                                                        "\n\nGrüße,\n\n" + person.contacts_information[0]

    # Texts, if the victim's hobby is known.
    def hobby_text(self,person):
        hobbie = str(person.hobbies).capitalize()
        self.subject = "Verbessere deine Techniken im Hobby "+hobbie
        self.text = "Hi "+person.first_name+",\ndamit du deine Leistung im Hobby "+hobbie+" verbessern kannst, musst " \
                    "du unbedingt die Techniken deiner Vorbilder anschauen!\nIm Anhang befindet sich eine kleine " \
                    "Übersicht.\n\nDein Team der deutschen Förderung"

    # Texts, if the victim's year of birth is known.
    def year_of_birth_text(self,person):
        year_of_birth = str(person.year_of_birth)
        print("YEAR", year_of_birth)
        if person.locations:
            location = str(person.locations).capitalize()
            self.subject = "Jahrgang "+year_of_birth+" - "+location
            self.text = "Hi "+ person.first_name+",\ndieses Jahr findet in "+location+" ein Treffen für alle Personen, " \
                        "die "+year_of_birth+" geboren sind, statt. Im Anhang befindet sich eine Liste mit den Leuten " \
                        "die bereits zugesagt haben.\n\nDein Orga-Team "+location
        else:
            self.subject = "Jahrgang " + year_of_birth
            self.text = "Hi " + person.first_name + ",\ndieses Jahr findet ein Treffen für alle Personen, die " \
                        + person.year_of_birth + " geboren sind, statt. Im Anhang befindet sich eine Liste mit den " \
                        "Leuten die bereits zugesagt haben.\n\nDein Orga-Team"

    # Texts, if the victim's location is known.
    def locations_text(self,person):
        if person.locations is not None:
            location = person.locations
        else:
            location = person.place_of_residence
        self.subject = "Streetfood-Festival in "+ location
        self.text = "Hi "+ person.first_name+"derzeit findet das erste STREETFOOD-FESTIVAL in "+ location + "" \
                    "statt. Im Anhang befindet sich der Plan, auf dem alles weitere erklärt wird.\n" \
                    "Wir freuen uns auf dich!\n\nDein Streefood-Team aus "+location
