from itertools import combinations, permutations

class CreateEmailAddresses:

    def __init__(self):
        self.firstname = ""
        self.secondname = ""
        self.year_of_birth = ""
        self.shortform_birthdate = ""
        self.localname = []
        self.underline = "_"
        self.point = "."
        self.formatted_localnames=[]
        self.email_list = []
        self.provider_list = ["web.de", "gmail.com", "gmx.de", "t-online.de", "freenet.de"]

    def create_email_addresses(self, person):
        self.firstname = person.first_name.replace("%22", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
        self.secondname = str(person.second_name).replace("%22", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
        self.year_of_birth = person.year_of_birth
        self.shortform_birthdate = str(person.year_of_birth)[-2:]
        # if all attributes are known
        if self.firstname and self.secondname and self.year_of_birth:
            firstname_secondname_list = [self.firstname, self.secondname]
            firstname_secondname_birthdate_list = [self.firstname,self.secondname,self.year_of_birth]
            firstname_secondname_shortform_list = [self.firstname, self.secondname, self.shortform_birthdate]

            self.localname.append(self.firstname)
            self.localname.append(self.secondname)

            self.create_permutations(firstname_secondname_list)
            self.create_permutations(firstname_secondname_birthdate_list)
            self.create_permutations(firstname_secondname_shortform_list)

        # year of birth is not known
        elif self.year_of_birth =="" and self.firstname and self.secondname:
            firstname_secondname_list = [self.firstname, self.secondname]
            self.localname.append(self.firstname)
            self.localname.append(self.secondname)
            self.create_permutations(firstname_secondname_list)

        # second name is not known
        elif self.secondname == "":
            firstname_year_of_birth_list = [self.firstname, self.year_of_birth]
            self.localname.append(self.firstname)
            self.create_permutations(firstname_year_of_birth_list)

        # first name is not known
        elif self.firstname == "":
            secondname_year_of_birth_list = [self.secondname, self.year_of_birth]
            self.localname.append(self.secondname)
            self.create_permutations(secondname_year_of_birth_list)

        self.create_localnames()
        self.create_final_email()

        return self.email_list

    def create_final_email(self):
        for localname in self.formatted_localnames:
            for provider in self.provider_list:
                string = localname+"@"+provider
                self.email_list.append(string)

    def create_localnames(self):
        if self.firstname:
            self.formatted_localnames.append(self.firstname)
        elif self.secondname:
            self.formatted_localnames.append(self.secondname)

        for element in self.localname:
            if isinstance(element,(list,tuple)):
                string_without = "".join(element)
                string_point = "".join(".").join(element)
                string_underline = "".join("_").join(element)
                string_minus = "".join("-").join(element)
                self.formatted_localnames.append(string_without)
                self.formatted_localnames.append(string_point)
                self.formatted_localnames.append(string_underline)
                self.formatted_localnames.append(string_minus)


    def create_permutations(self,list):
        permutation_list = permutations(list)
        for perm in permutation_list:
            self.localname.append(perm)
