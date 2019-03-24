import csv


class CreateSearchLink:
    class Person(object):
        def __init__(self):
            self.first_name = ""
            self.second_name = ""
            self.place_of_residence = ""
            self.year_of_birth = ""
            self.estimated_year_of_birth = ""
            self.instagram_name = ""
            self.facebook_name = ""
            self.twitter_name = ""
            self.institution = ""

    def __init__(self):
        self.institution_key = 4
        self.location_key = 5
        self.year_of_birth_key = 6
        self.location_year_key = 7
        self.location_institution_key = 8
        self.location_year_institution_key = 9
        self.search_link_list = []
        self.person_object = self.Person()

    """def enter_information(self):
        self.person_object.first_name = input("Vorname: ").replace(" ","%22")
        self.person_object.second_name = input("Nachname: ").replace(" ","%22")
        self.person_object.location = input("Wohnort: ").replace(" ","%22")
        self.person_object.year_of_birth = input("Genaues Geburtsjahr: ").replace(" ","%22")
        self.person_object.estimated_year_of_birth = input("Geschätztes Geburtsjahr: ").replace(" ","%22")
        self.person_object.institution = input("Institution: ").replace(" ","%22")
        # self.person_object.instagram_name = input("Instagram Benutzername: ")
        # self.person_object.facebook_name = input("Facebook Benutzername: ")
        # self.person_object.twitter_name = input("Twitter Benutzername")

        return self.person_object
"""
    def get_search_links(self, person_object):
        if person_object.first_name and person_object.second_name is not "":
            if person_object.place_of_residence is not "":
                self.build_search_string(self.location_key)
                if person_object.year_of_birth is not "":
                    self.build_search_string(self.location_year_key)
                    if person_object.institution is not "":
                        self.build_search_string(self.location_year_institution_key)
                if person_object.institution is not "":
                    self.build_search_string(self.location_institution_key)
            if person_object.year_of_birth is not "":
                self.build_search_string(self.year_of_birth_key)
            if person_object.institution is not "":
                self.build_search_string(self.institution_key)
        # location kann gespeichert werden damit auf einer Webseite danach gesucht werden kann. Ode zu städte liste hinzufügen

        return self.search_link_list

    def build_search_string(self, key):
        """if key == self.facebook_key:
            search_string = ""
            self.search_link_list.append(search_string)

        if key == self.instagram_key:
            search_string = "https://www.instagram.com/" + self.person_object.instagram_name + "/"
            self.search_link_list.append(search_string)

        if key == self.twitter_key:
            search_string = "https://twitter.com/search?f=users&q=%20" + self.person_object.first_name + "%20" + \
                            self.person_object.second_name
            self.search_link_list.append(search_string)"""

        if key == self.location_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22" + self.person_object.place_of_residence + "%22"
            self.search_link_list.append(search_string)

        if key == self.year_of_birth_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22"+ self.person_object.year_of_birth + "%22"
            self.search_link_list.append(search_string)

        if key == self.institution_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22"+self.person_object.institution + "%22"
            self.search_link_list.append(search_string)

        if key == self.location_year_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22" + self.person_object.place_of_residence + "%22+" + "%22" \
                            + self.person_object.year_of_birth + "%22"
            self.search_link_list.append(search_string)

        if key == self.location_institution_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22" + self.person_object.place_of_residence + "%22+" + "%22" \
                            + self.person_object.institution + "%22"
            self.search_link_list.append(search_string)

        if key == self.location_year_institution_key:
            search_string = "https://www.google.com/search?q=%22" + self.person_object.first_name + "+" \
                            + self.person_object.second_name + "%22+" + "%22" + self.person_object.place_of_residence + "%22+" + "%22" \
                            + self.person_object.year_of_birth + "%22+" + "%22" + self.person_object.institution + "%22"
            self.search_link_list.append(search_string)
"""
person_object = enter_information()
analyze_information(person_object)
print(search_link_list)
test = CreateSearchLink()
test.enter_information()
"""