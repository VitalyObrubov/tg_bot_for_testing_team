import re

def is_email(email: str):
    email = email.replace(" ", "")
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if email_regex.match(email):
        return email
    else:
        return False

def is_mak(mac: str):
    mac = mac.replace(" ", "")
    mac = mac.upper()
    mac = mac.replace("А", "A") # рус в англ
    mac = mac.replace("В", "B")
    mac = mac.replace("С", "C")
    mac = mac.replace("Е", "E")
    mac = mac.replace("O", "0") # О англ в 0
    mac = mac.replace("О", "0") # О рус в 0
 

    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        return mac
    else:
        return False