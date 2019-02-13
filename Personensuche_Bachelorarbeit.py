
class Person(object):
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.location = ""
        self.year_of_birth = ""
        self.instagram_name = ""
        self.facebook_name = ""
        self.twitter_name = ""
        self.company = ""


def enter_information():
    person_object = Person()
    person_object.first_name = input("Vorname: ")
    person_object.second_name = input("Nachname: ")
    person_object.location = input("Wohnort: ")
    person_object.year_of_birth = input("Geburtsjahr auch grobes Geburtsjahr: ")
    #person_object.instagram_name = input("Instagram Benutzername: ")
    #person_object.facebook_name = input("Facebook Benutzername: ")
    #person_object.twitter_name = input("Twitter Benutzername")
    #person_object.company = input("Arbeitgeber: ")
    return person_object


def analyze_information(person_object):
    if person_object.instagram_name is not "":
        print("Instagram name is not none")
        # TODO build string
    if person_object.facebook_name is not "":
        print("Facebook name is not none")
        # TODO build string
    if person_object.twitter_name is not "":
        print("Twitter name is not none")
        # TODO build string
    if person_object.first_name and person_object.second_name is not "":
        print("Firstname and Secondname are not none")
        if person_object.location is not "":
            print("location auch bekannt")
            #TODO build string for searchengine
            #location kann gespeichert werden damit auf einer Webseite danach gesucht werden kann. Ode zu städte liste hinzufügen
            build_search_string(person_object, "location")


def build_search_string(person_object, key):
    if key == "location":
        search_string = "https://www.google.com/search?q=%22"+person_object.first_name+"+"+person_object.second_name+"%22+"+person_object.location
        print(search_string)
    if key == "facebook":
        print("facebook")
        # search_string =

person_object = enter_information()
analyze_information(person_object)
