from itertools import combinations, permutations

class CreateEmailAddresses:

    def __init__(self):
        self.firstname = ""
        self.secondname = ""
        self.birthdate = ""
        self.shortform_birthdate = ""
        self.localname = []
        self.underline = "_"
        self.point = "."
        self.formatted_localnames=[]
        self.email_list = []
        self.provider_list = ["web.de","gmail.com", "freemail.de"]

    def create_email_addresses(self, firstname,secondname,birthdate, shortform_birthdate):
        self.firstname = firstname
        self.secondname = secondname
        self.birthdate = birthdate
        self.shortform_birthdate = shortform_birthdate

        firstname_secondname_list = [self.firstname, self.secondname]
        firstname_secondname_birthdate_list = [self.firstname,self.secondname,self.birthdate]
        firstname_secondname_shortform_list = [self.firstname, self.secondname, self.shortform_birthdate]

        # Maybe Delete!
        """info_set = { self.firstname, self.secondname, self.birthdate}
        collect = set()
        step = {''}
        while step:
            # step = set(a+b for a in step for b in S if len(a+b) <= 24)
            step = set( a+b for a in step for b in info_set if len(a + b) <= 24 and not b in a)
            collect |= step
        print(sorted(collect))
        """
        self.localname.append(self.firstname)
        self.localname.append(self.secondname)

        self.create_permutations(firstname_secondname_list)
        self.create_permutations(firstname_secondname_birthdate_list)
        self.create_permutations(firstname_secondname_shortform_list)

        self.create_localnames()
        self.create_final_email()
        print("Localnames: ",self.localname)
        print("Formatted Localnames: ",self.formatted_localnames)
        print("EMAIL",self.email_list)

    def create_final_email(self):
        for localname in self.formatted_localnames:
            for provider in self.provider_list:
                string = localname+"@"+provider
                self.email_list.append(string)

    def create_localnames(self):
        print("create local name")
        self.formatted_localnames.append(self.firstname)
        self.formatted_localnames.append(self.secondname)

        for element in self.localname:
            if isinstance(element,(list,tuple)):
                string_without = "".join(element)
                string_point = "".join(".").join(element)
                string_underline = "".join("_").join(element)
                self.formatted_localnames.append(string_without)
                self.formatted_localnames.append(string_point)
                self.formatted_localnames.append(string_underline)


    def create_permutations(self,list):
        #TODO create Permutations
        permutation_list = permutations(list)
        for perm in permutation_list:
            self.localname.append(perm)
        #print(list(combinations(mylist,2)))


"""
player_information_list = []
no_birth_date = '()'
def get_player_information_from_csvfile():
    with open('linksToPlayerFile.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        included_cols = [0,1, 2, 5]
        for row in reader:
            content = list(row[i] for i in included_cols)
            player_information_list.append(content)
        #print(player_information_list)
        for element in player_information_list:
            create_mail(element)
    csvFile.close()
def formate_birth_date(birth_date):
    formatted_birth_date = birth_date.split()[0]
    if formatted_birth_date == no_birth_date:
        year_of_birth = no_birth_date
    else:
        year_of_birth = formatted_birth_date.split(".")[2]
    return year_of_birth

def create_mail(player_information):
    first_name = player_information[0]
    second_name = player_information[1]
    last_name = player_information[2]
    year_of_birth = formate_birth_date(player_information[3])

    print(first_name, second_name, last_name, year_of_birth)


S = {'firstname', 'secondname', '1995'}

collect = set()
step = {''}
while step:
    '''for a in step:
        for b in S:
            if len(a+b)<=24:
                if not a==b:
                    step.add(a+b)
'''
    # step = set(a+b for a in step for b in S if len(a+b) <= 24)
    step = set(a+b for a in step for b in S if len(a+b)<=24 and not b in a)

    collect |= step

print(sorted(collect))

#get_player_information_from_csvfile()
"""
email = CreateEmailAddresses()
email.create_email_addresses("marco","lang", "1995", "95")