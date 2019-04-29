

# In this class the search links for google are created.
class CreateSearchLink:

    def __init__(self):
        self.email_key = 3
        self.institution_key = 4
        self.location_key = 5
        self.year_of_birth_key = 6
        self.location_year_key = 7
        self.location_institution_key = 8
        self.location_year_institution_key = 9
        self.search_link_list = []

    # check with which data the search links are generated
    def get_search_links(self, person_object):
        if person_object.input_email is not "":
            self.build_search_string(self.email_key, person_object)
        if person_object.first_name and person_object.second_name is not "":
            if person_object.place_of_residence is not "":
                self.build_search_string(self.location_key, person_object)
                if person_object.year_of_birth is not "":
                    self.build_search_string(self.location_year_key, person_object)
                    if person_object.institution is not "":
                        self.build_search_string(self.location_year_institution_key, person_object)
                if person_object.institution is not "":
                    self.build_search_string(self.location_institution_key, person_object)
            if person_object.year_of_birth is not "":
                self.build_search_string(self.year_of_birth_key, person_object)
            if person_object.institution is not "":
                self.build_search_string(self.institution_key, person_object)
        return self.search_link_list

    # generate seach links
    def build_search_string(self, key, person_object):
        if key == self.email_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.input_email + "%22"
            self.search_link_list.append(search_string)

        elif key == self.location_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22" + person_object.place_of_residence + "%22"
            self.search_link_list.append(search_string)

        elif key == self.year_of_birth_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22"+ person_object.year_of_birth + "%22"
            self.search_link_list.append(search_string)

        elif key == self.institution_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22"+person_object.institution + "%22"
            self.search_link_list.append(search_string)

        elif key == self.location_year_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22" + person_object.place_of_residence + "%22+" + "%22" \
                            + person_object.year_of_birth + "%22"
            self.search_link_list.append(search_string)

        elif key == self.location_institution_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22" + person_object.place_of_residence + "%22+" + "%22" \
                            + person_object.institution + "%22"
            self.search_link_list.append(search_string)

        elif key == self.location_year_institution_key:
            search_string = "https://www.google.com/search?q=%22" + person_object.first_name + "+" \
                            + person_object.second_name + "%22+" + "%22" + person_object.place_of_residence + "%22+" + "%22" \
                            + person_object.year_of_birth + "%22+" + "%22" + person_object.institution + "%22"
            self.search_link_list.append(search_string)