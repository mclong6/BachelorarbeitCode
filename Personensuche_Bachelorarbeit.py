

instagram_key = 1
facebook_key = 2
twitter_key = 3
institution_key = 4
location_key = 5
year_of_birth_key = 6
location_year_key = 7
location_institution_key = 8
location_year_institution_key = 9


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
        self.institution = ""


def enter_information():
    person_object = Person()
    person_object.first_name = input("Vorname: ").replace(" ","%22")
    person_object.second_name = input("Nachname: ").replace(" ","%22")
    person_object.location = input("Wohnort: ").replace(" ","%22")
    person_object.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ","%22")
    person_object.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ","%22")
    person_object.institution = input("Institution: ").replace(" ","%22")
    #person_object.instagram_name = input("Instagram Benutzername: ")
    #person_object.facebook_name = input("Facebook Benutzername: ")
    #person_object.twitter_name = input("Twitter Benutzername")

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
        if person_object.location is not "":
            build_search_string(person_object, location_key)
            if person_object.year_of_birth is not "":
                build_search_string(person_object,location_year_key)
                if person_object.institution is not "":
                    build_search_string(person_object, location_year_institution_key)
            if person_object.institution is not "":
                build_search_string(person_object,location_institution_key)
        if person_object.year_of_birth is not "":
            build_search_string(person_object, year_of_birth_key)
        if person_object.institution is not "":
            build_search_string(person_object, institution_key)
    #location kann gespeichert werden damit auf einer Webseite danach gesucht werden kann. Ode zu städte liste hinzufügen


def build_search_string(person_object, key):
    if key == facebook_key:
        search_string = ""
        search_link_list.append(search_string)

    if key == instagram_key:
        search_string = "https://www.instagram.com/" + person_object.instagram_name + "/"
        search_link_list.append(search_string)

    if key == twitter_key:
        search_string = "https://twitter.com/search?f=users&q=%20" + person_object.first_name + "%20" + \
                        person_object.second_name
        search_link_list.append(search_string)

    if key == location_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + "%22" + person_object.location + "%22"
        search_link_list.append(search_string)

    if key == year_of_birth_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + "%22"+person_object.year_of_birth + "%22"
        search_link_list.append(search_string)

    if key == institution_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + "%22"+person_object.institution + "%22"
        search_link_list.append(search_string)

    if key == location_year_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + "%22"+person_object.location + "%22+" + "%22" \
                        + person_object.year_of_birth + "%22"
        search_link_list.append(search_string)

    if key == location_institution_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                        + person_object.second_name + "%22+" + "%22" + person_object.location + "%22+" + "%22" \
                        + person_object.institution + "%22"
        search_link_list.append(search_string)

    if key == location_year_institution_key:
        search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                    + person_object.second_name + "%22+" + "%22" + person_object.location + "%22+" + "%22" \
                    + person_object.year_of_birth + "%22+" + "%22" + person_object.institution + "%22"
        search_link_list.append(search_string)


person_object = enter_information()
analyze_information(person_object)
print(search_link_list)
