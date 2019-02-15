

instagram_key = 1
facebook_key = 2
twitter_key = 3
firstname_secondname_key = 4
lfirstname_secondname_location_key = 5
firstname_secondname_year_key = 6
firstname_secondname_location_year_key = 7

search_link_list = []

class Person(object):
    def __init__(self):
        self.first_name = ""
        self.second_name = ""
        self.location = ""
        self.year_of_birth = ""
        self.estimated_year_of_birth = ""
        self.instagram_name = ""
        self.facebook_name = ""
        self.twitter_name = ""
        self.company = ""


def enter_information():
    person_object = Person()
    person_object.first_name = input("Vorname: ")
    person_object.second_name = input("Nachname: ")
    person_object.location = input("Wohnort: ")
    person_object.year_of_birth = input("Genaues Geburtsjahr: ")
    person_object.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ")

    #person_object.instagram_name = input("Instagram Benutzername: ")
    #person_object.facebook_name = input("Facebook Benutzername: ")
    #person_object.twitter_name = input("Twitter Benutzername")
    #person_object.company = input("Arbeitgeber: ")
    return person_object


def analyze_information(person_object):
    if person_object.instagram_name is not "":
        print("Instagram name is not none")
        build_search_string(person_object,instagram_key)
    if person_object.facebook_name is not "":
        print("Facebook name is not none")
        build_search_string(person_object,facebook_key)
    if person_object.twitter_name is not "":
        print("Twitter name is not none")
        build_search_string(twitter_key)
    if person_object.first_name and person_object.second_name is not "":
        build_search_string(person_object, firstname_secondname_key)
        if person_object.location is not "":
            build_search_string(person_object, lfirstname_secondname_location_key)
            if person_object.year_of_birth is not "":
                build_search_string(person_object,firstname_secondname_location_year_key)
        if person_object.year_of_birth is not "":
            build_search_string(person_object, firstname_secondname_year_key)
    #location kann gespeichert werden damit auf einer Webseite danach gesucht werden kann. Ode zu städte liste hinzufügen


def build_search_string(person_object, key):
    if key == facebook_key:
        search_string = ""
        search_link_list.append(search_string)

    if key == instagram_key:
        search_string = "https://www.instagram.com/" + person_object.instagram_name + "/"
        search_link_list.append(search_string)

    if key == twitter_key:
        search_string = "https://twitter.com/search?f=users&q=%20" + person_object.first_name + "%20" + person_object.second_name
        search_link_list.append(search_string)

    if key == firstname_secondname_key:
        search_string = "https://www.google.com/search?q=%22"+ person_object.first_name+"+"\
                        + person_object.second_name+"%22"
        search_link_list.append(search_string)

    if key == lfirstname_secondname_location_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + person_object.location
        search_link_list.append(search_string)

    if key == firstname_secondname_year_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + person_object.year_of_birth
        search_link_list.append(search_string)
    if key == firstname_secondname_location_year_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + person_object.location + "+" \
                        + person_object.year_of_birth
        search_link_list.append(search_string)


person_object = enter_information()
analyze_information(person_object)
print(search_link_list)
