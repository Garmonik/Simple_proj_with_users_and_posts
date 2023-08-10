import re
import string
import secrets


def generate_password():
    valid_characters = string.ascii_letters + string.digits + string.punctuation.replace("'", "").replace('"', '')
    password = [secrets.choice(valid_characters) for _ in range(20)]
    password[secrets.randbelow(15)] = secrets.choice(string.ascii_uppercase)
    password[secrets.randbelow(15)] = secrets.choice(string.punctuation.replace("'", "").replace('"', ''))

    secrets.SystemRandom().shuffle(password)
    final_password = ''.join(password)

    return final_password


def validation_username(username):
    errors = []

    # Проверка на пустоту имени
    if not username or username == "":
        errors.append("Username can't be empty")

    # Проверка длины имени
    if len(username) > 50:
        errors.append("Username can't exceed 50 characters")

    # Проверка на наличие запрещенных символов
    forbidden_characters = ["'", '"']
    for char in forbidden_characters:
        if char in username:
            errors.append("Username can't contain the characters ' or \"")
    return errors


def validation_password(password, passwordagain):
    errors = []

    # Проверка на пустоту пароля
    if not password or password == "":
        errors.append("Password can't be empty")

    # Проверка длины пароля
    if len(password) < 5:
        errors.append("Password cannot be less than 5 characters")

    # Проверка на наличие запрещенных символов
    forbidden_characters = ["'", '"']
    for char in forbidden_characters:
        if char in password:
            errors.append("Password can't contain the characters ' or \"")

    # Проверка на наличие хотя бы одной буквы в верхнем регистре
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    # Проверка на наличие хотя бы одного из указанных символов
    special_characters = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "{", "}", "[", "]", "-", "=", "+", "_", "|", "\\", "/", "№", ";", ":", ",", ".", "?", "<", ">"]
    if not any(char in password for char in special_characters):
        errors.append("The password must contain at least one of the following characters: ! @ # $ % ^ & * ( ) { } [ ] - = + _ | \\ / № ; : , . ? < >")

    # Проверка на совпадение password и passwordagain
    if password != passwordagain:
        errors.append("Password and Passwordagain don't match")
    return errors


def validate_email_format(email):
    errors = []

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        errors.append("Email entered incorrectly")
    return errors