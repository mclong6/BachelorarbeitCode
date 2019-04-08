
class CreateEmailText:

    def __init__(self):
        print("Initialize CreatEmailTextClass")
        self.text = ""

    def create_email_text(self, person):

        print("CREATE_EMAIL_TEXT")
        person.first_name = str(person.first_name).replace("%22", "")
        person.second_name = str(person.second_name).replace("%22", "")

        if person.contacts_information:
            self.text = self.contacts_information_text(person)
        elif person.universities:
            self.text = self.university_text(person)
        return self.text

    def contacts_information_text(self,person):
        splitted_string_name = str(person.contacts_information[0]).split()
        if len(person.contacts_information)>=2:
            if len(splitted_string_name)>=2:
                text = "Hallo "+person.first_name+",\nhier ist "+splitted_string_name[0]+". Ich schreib dir wegen dem "+ \
                   person.contacts_information[1]+".\n\nGrüße,\n\n" + person.contacts_information[0]
            else:
                text = "Hallo "+person.first_name+",\nhier ist "+person.contacts_information[0]+". Ich schreib dir wegen dem "+ \
                   person.contacts_information[1]+".\n\nGrüße,\n\n" + person.contacts_information[0]
        else:
            text = "Hallo " + person.first_name + ", Ich schreib dir wegen dem Problem von gestern.\nViele Grüße,\n\n"
        return text

    def university_text(self, person):
        text = "Hallo "+person.first_name+",\ndu musst dich erneut zurückmelden.\n\nMif freundlichen Grüßen\n\n"+ \
                  "Dein Team der "+person.universities[0]
        return text