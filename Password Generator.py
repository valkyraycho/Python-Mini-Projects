import random
import string


def generate_password(min_length, digit_required=True, special_char_required=True):
    digits = string.digits
    letters = string.ascii_letters
    special_chars = string.punctuation
    password = ""

    chars = ""
    chars += letters
    if digit_required:
        chars += digits
    if special_char_required:
        chars += special_chars

    has_digit = False
    has_special_char = False
    meet_criteria = False

    while not meet_criteria or len(password) < min_length:
        char = random.choice(chars)
        password += char

        has_digit = has_digit or char in digits
        has_special_char = has_special_char or char in special_chars

        # set to True first and check the conditions
        meet_criteria = True
        if digit_required:
            meet_criteria = has_digit
        if special_char_required:
            meet_criteria = meet_criteria and has_special_char

    return password


min_length = int(input("Enter the minimum length: "))
digit_required = input("Do you want to have digits? [y/n] ").lower() == 'y'
special_char_required = input("Do you want to have special characters? [y/n] ").lower() == 'y'

print(generate_password(min_length, digit_required, special_char_required))
