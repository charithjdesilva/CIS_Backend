import re
from typing import Optional
import bcrypt
import random

# Generate a random 4-digit code
random_code = random.randint(1000, 9999)

# Convert the code to a string (if needed)
random_code_str = str(random_code)

# print(random_code_str)

# print("Random 4-Digit Code:", random_code_str)

def do_hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Example usage:
# password = "my_secure_password"
# hashed_password = hash_password(password)
# print("Hashed Password:", hashed_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def is_valid_password(password, new_password):
    if(password == new_password):
        # Check for at least one uppercase and one lowercase letter
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\\-]', password):
            return False

        return True
    
    return False


def is_valid_email(email):
    # Regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Use re.match to find a match at the beginning of the string
    match = re.match(pattern, email)
    
    # If match is not None, the email is valid
    return match is not None

# Example usage:
email = "example@email.com"
# if is_valid_email(email):
#     print(f"{email} is a valid email address.")
# else:
#     print(f"{email} is not a valid email address.")



# # Sample hardcoded users (In practice, use a database)
# hardcoded_users = [
#     {"username": "user1", "password": "password1"},
#     {"username": "user2", "password": "password2"},
# ]

# def authenticate_user(username: str, password: str):
#     for user_data in hardcoded_users:
#         if user_data["username"] == username and user_data["password"] == password:
#             return User(**user_data)
#     return None




def is_valid_sri_lankan_mobile_number(number):
    # Regular expression pattern for a valid Sri Lankan mobile number
    pattern = r'^(07[0-9]|0[7-9][0-9]{2})[0-9]{7}$'
    
    # Use re.match to find a match at the beginning of the string
    match = re.match(pattern, number)
    
    # If match is not None, the number is valid
    return match is not None

# Example usage:
number = "0771234567"
# if is_valid_sri_lankan_mobile_number(number):
#     print(f"{number} is a valid Sri Lankan mobile number.")
# else:
#     print(f"{number} is not a valid Sri Lankan mobile number.")
