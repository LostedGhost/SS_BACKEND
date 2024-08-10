from api.config import *
from datetime import datetime, timedelta
import random
import string
import requests


def generate_string(length=12):
    """Generate a strong password."""
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    # Combine character sets
    all_characters = lowercase_letters + uppercase_letters + digits

    # Ensure at least one character from each set
    password = random.choice(lowercase_letters)
    password += random.choice(uppercase_letters)
    password += random.choice(digits)

    # Fill remaining length with random characters
    for _ in range(length - 3):
        password += random.choice(all_characters)

    # Shuffle the password to make it more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

def chiffrement(message) -> str:
    decalage = KEY
    message_chiffre = ""
    for caractere in message:
        # Vérifier si le caractère est une lettre majuscule
        if caractere.isupper():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('A') + decalage) % 26 + ord('A')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est une lettre minuscule
        elif caractere.islower():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('a') + decalage) % 26 + ord('a')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est un chiffre
        elif caractere.isdigit():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('0') + decalage) % 10 + ord('0')
            message_chiffre += chr(nouveau_code)
        # Si le caractère est un caractère spécial, le laisser inchangé
        else:
            message_chiffre += caractere
    return message_chiffre

def is_strong_password(password):
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation
    ll = False
    ul = False
    d = False
    sc = False
    for el in password:
        if el in lowercase_letters and not ll:
            ll = True
        elif el in uppercase_letters and not ul:
            ul = True
        elif el in digits and not d:
            d = True
        elif el in special_characters and not sc:
            sc = True
        if ll and ul and d and sc:
            break
    return ll and ul and d and sc and len(password) >= 8

def date_to_text(date):
    return date.strftime('%Y-%m-%d')

def full_date_to_text(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def text_to_date(text):
    return datetime.datetime.strptime(text, '%Y-%m-%d')

def is_valid_email(email):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=3155d505c0df557f9d5bb1b8a0b983ff918587dd"
    response = requests.get(url)
    data = response.json().get('data')
    status = data.get('status', None)
    return status == "valid"

def is_valid_phone_number(phone_number):
    url = f"https://apilayer.net/api/validate?access_key=10e397d499e56288cc79ac29f49e6682&number={phone_number}&country_code=&format=1"
    response = requests.get(url).json()
    valid = response.get('valid')
    return valid

