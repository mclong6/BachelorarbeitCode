from difflib import SequenceMatcher

def compare_email_with_name(firstname, secondname, mail):
    formatted_name = firstname.lower() + secondname.lower()
    local_part_of_mailaddress = mail.split("@")[0].lower()
    percentage_limit = 0.4
    print(SequenceMatcher(None, formatted_name, local_part_of_mailaddress).ratio())

compare_email_with_name("Max","Mustermann","MusterMax@gmx.com")