from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from django.core.exceptions import ValidationError
import re

def is_valid_string(field):
    if not isinstance(field, str):
        raise ValidationError("Invalid input: not a string")

    allowed_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,@()-:/- –?&!")
    invalid_characters = [c for c in field if c not in allowed_characters]
    if invalid_characters:
        invalid_char = invalid_characters[0]
        raise ValidationError(f"Invalid input: contains invalid character '{invalid_char}'")
    return True

def is_valid_mail(email):
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')      # regex pattern for email
    match = pattern.match(email)
    if match:
        return True
    else:
        raise ValidationError("Email address is not valid.")

def is_valid_password(password):
    print(password)
    if len(password) < 8 or len(password) == 0:
        raise ValidationError("Password length should be greater than 8")
    if not any(c.isupper() for c in password):
        raise ValidationError("Password should contain a uppercase letter")
    if not any(c.islower() for c in password):
        raise ValidationError("Password should contain a lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password should contain a digit")
    if not any(c in "!@#$%^&*()-+?_=,<>/:" for c in password):
        raise ValidationError("Password should contain a special character")
    return True

def is_valid_timestamp(value):
    pattern = r'^\d{14}$' 
    if not re.match(pattern, value):
        raise ValidationError('Invalid timestamp format. It should be YYYYMMDDHHMMSS.')


