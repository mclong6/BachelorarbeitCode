import csv


class GatherInformation:

    def __init__(self):
        self.database_word_list_hobbies = []
        self.database_word_list_location = []
        self.database_word_list_occupation = []
        self.database_word_list_universities = []
        self.location = []
        self.hobbies = []
        self.occupation = []
        self.university = []

    def compare_keywords_with_databases(self, keywords):
        print(keywords)
        with open('location.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_location.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_location:
                    #if element in word:
                    if element == word:
                        if word not in self.location:
                            print("Textwort: " + word + "\nWort aus Städte-Liste: " + element)
                            self.location.append(element)


        with open('hobbies.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_hobbies.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_hobbies:
                    #if element in word:
                    if element == word:
                        if word not in self.hobbies:
                            print("Textwort: " + word + "\nWort aus Hobby-Liste: " + element)
                            self.hobbies.append(element)

        with open('occupation.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_occupation.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_occupation:
                    #if element in word:
                    if element == word:
                        if word not in self.occupation:
                            print("Textwort: " + word + "\nWort aus Occupation-Liste: " + element)
                            self.occupation.append(element)

        with open('universities.csv', 'r') as csvFile:
            # with open('hobbies.csv', 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            for row in csv_reader:
                self.database_word_list_universities.append(row[0].lower())
            for word in keywords:
                for element in self.database_word_list_universities:
                    #if element in word:
                    if element == word:
                        if word not in self.university:
                            print("Textwort: " + word + "\nWort aus Universities-Liste: " + element)
                            self.university.append(element)
        #TODO Vereinskürzel hinzufügen

        with open("person_information.csv", "a") as file:
            fieldnames = ["firstname", "secondname", "location", "year_of_birth", "estimated_year_of_birth",
                          "institution", "email", "hobbies", "occupation", "universities"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # writer.writeheader()
            if self.hobbies is not "":
                writer.writerow({"hobbies": self.hobbies})

        print("Location:", self.location)
        print("Hobbies: ", self.hobbies)
        print("Occupation", self.occupation)
        print("University", self.university)
