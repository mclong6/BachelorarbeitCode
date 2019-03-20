
class CreateEmailContent:

    def __init__(self):
        print("Initialize CreatEmailContentClass")

    def university_content(self, university):
        print("University: ", university)

        content = "Hallo Name,\n du musst dich erneut zurückmelden.\n Mif freundlichen Grüßen\n\n"+ \
                  "Dein Team der"+university
